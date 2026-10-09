from contextlib import asynccontextmanager
from database import engine
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import SQLModel, Session, select

from database import create_db_and_tables, engine
from models import User, PostureBaseline, HomePosition
from schemas import (UserCreate, UserPublic, UserLogin, Token, HomePositionPublic, HomeSaveRequest, MotorJogRequest, PostureBaselineData, PostureBaselinePublic, CurrentPostureData, PostureComparisonPublic)
from security import hash_password, verify_password, create_access_token
from security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.communication.stm32_client import STM32Client
from app.communication.stm32_simulator import STM32Simulator
import serial

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

USE_STM32_SIMULATOR = False


def build_jog_data(axis: int, delta_deg: float) -> bytes:
    delta_x10 = int(delta_deg * 10)

    axis_byte = axis.to_bytes(
        1,
        byteorder="big",
        signed=False,
    )

    delta_bytes = delta_x10.to_bytes(
        2,
        byteorder="big",
        signed=True,
    )

    return axis_byte + delta_bytes



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    stm32 = None

    try:
        if USE_STM32_SIMULATOR:
            stm32 = STM32Simulator()
            stm32.start()

        else:
            client = STM32Client(
                port = os.environ["STM32_PORT"],
                baud=115200,
            )


            try:
                client.start()
                stm32 = client

                print("STM32 CONNECTED")

            except serial.SerialException as e:
                print("STM32 NOT CONNECTED")
                print(e)

        app.state.stm32 = stm32

        yield

    finally:
        if stm32 is not None:
            stm32.close()


app = FastAPI(lifespan=lifespan)

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효한 로그인이 필요합니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_error

    username = decode_access_token(credentials.credentials)

    if username is None:
        raise credentials_error

    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        if user is None:
            raise credentials_error

        return user

@app.post(
    "/signup",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def signup(user_data: UserCreate):
    with Session(engine) as session:
        statement = select(User).where(User.username == user_data.username)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 아이디입니다.",
            )

        new_user = User(
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user



@app.post("/login", response_model=Token)
def login(login_data: UserLogin):
    with Session(engine) as session:
        statement = select(User).where(User.username == login_data.username)
        user = session.exec(statement).first()

        if user is None or not verify_password(
            login_data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="아이디 또는 비밀번호가 올바르지 않습니다.",
            )


        access_token = create_access_token(user.username)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }



@app.get("/users/me", response_model=UserPublic)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user
@app.get("/")
def read_root():
    return {"message": "Smart Monitor Arm Backend"}



@app.put(
    "/users/me/posture-baseline",
    response_model=PostureBaselinePublic,
)
def save_posture_baseline(
    baseline_data: PostureBaselineData,
    current_user: User = Depends(get_current_user),
):
    with Session(engine) as session:
        statement = select(PostureBaseline).where(
            PostureBaseline.user_id == current_user.id
        )
        baseline = session.exec(statement).first()

        if baseline is None:
            baseline = PostureBaseline(
                user_id=current_user.id,
                nose_x=baseline_data.nose_x,
                nose_y=baseline_data.nose_y,
                face_box_width=baseline_data.face_box_width,
                face_box_height=baseline_data.face_box_height,
            )
        else:
            baseline.nose_x = baseline_data.nose_x
            baseline.nose_y = baseline_data.nose_y
            baseline.face_box_width = baseline_data.face_box_width
            baseline.face_box_height = baseline_data.face_box_height

        session.add(baseline)
        session.commit()
        session.refresh(baseline)

        return baseline



@app.get(
    "/users/me/posture-baseline",
    response_model=PostureBaselinePublic,
)
def get_posture_baseline(
    current_user: User = Depends(get_current_user),
):
    with Session(engine) as session:
        statement = select(PostureBaseline).where(
            PostureBaseline.user_id == current_user.id
        )
        baseline = session.exec(statement).first()

        if baseline is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="저장된 기준 자세가 없습니다.",
            )

        return baseline




@app.post(
    "/users/me/posture-comparison",
    response_model=PostureComparisonPublic,
)
def compare_posture(
    current_data: CurrentPostureData,
    current_user: User = Depends(get_current_user),
):
    with Session(engine) as session:
        statement = select(PostureBaseline).where(
            PostureBaseline.user_id == current_user.id
        )
        baseline = session.exec(statement).first()

        if baseline is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="비교할 기준 자세가 없습니다.",
            )

        return PostureComparisonPublic(
            nose_x_error=round(
                current_data.nose_x - baseline.nose_x,
                4,
            ),
            nose_y_error=round(
                current_data.nose_y - baseline.nose_y,
                4,
            ),
            face_box_width_error=round(
                current_data.face_box_width - baseline.face_box_width,
                4,
            ),
            face_box_height_error=round(
                current_data.face_box_height - baseline.face_box_height,
                4,
            ),
        )


@app.post("/api/motor/jog")
def motor_jog(
    jog_data: MotorJogRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    stm32: STM32Client = request.app.state.stm32

    if stm32 is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="STM32가 연결되어 있지 않습니다.",
        )


    success = stm32.jog(
        jog_data.axis,
        jog_data.delta_deg,
    )

    if success:
        return {
            "success": True,
            "axis": jog_data.axis,
            "delta_deg": jog_data.delta_deg,
        }

    if stm32.last_command_error_code is not None:
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "error_code": stm32.last_command_error_code,
                "error": stm32.last_command_error_name,
            },
        )

    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error_code": None,
            "error": "STM32_COMMAND_FAILED",
        },
    )


@app.post("/api/motor/clear-error")
def motor_clear_error(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    stm32: STM32Client = request.app.state.stm32
    if stm32 is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="STM32가 연결되어 있지 않습니다.",
    )

    success = stm32.clear_error()
    if success:
        return {
            "success": True,
            "message": "STM32 error cleared",
        }

    if stm32.last_command_error_code is not None:
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "error_code": stm32.last_command_error_code,
                "error": stm32.last_command_error_name,
            },
        )

    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error_code": None,
            "error": "STM32_CLEAR_ERROR_FAILED",
        },
    )


@app.post("/api/motor/set-home")
def motor_set_home(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    stm32: STM32Client = request.app.state.stm32
    if stm32 is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="STM32가 연결되어 있지 않습니다.",
        )

    success=stm32.set_home()

    if success:
        return{
            "success": True,
            "message": "STM32 HOME saved",
        }

    if stm32.last_command_error_code is not None:
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "error_code": stm32.last_command_error_code,
                "error": stm32.last_command_error_name,
            },
        )

    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error_code": None,
            "error": "STM32_SET_HOME_FAILED",
        },
    )


@app.post("/api/motor/move-home")
def motor_move_home(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    stm32: STM32Client = request.app.state.stm32
    if stm32 is None:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="STM32가 연결되어 있지 않습니다.",
            )

    success = stm32.move_home()

    if success:
        return {
            "success": True,
            "message": "STM32 moved to HOME",
        }

    if stm32.last_command_error_code is not None:
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "error_code": stm32.last_command_error_code,
                "error": stm32.last_command_error_name,
            },
        )

    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error_code": None,
            "error": "STM32_MOVE_HOME_FAILED",
        },
    )



@app.post(
    "/api/home/save",
    response_model=HomePositionPublic,
)
def save_home_position(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효한 사용자가 아닙니다.",
        )

    stm32: STM32Client = request.app.state.stm32
    if stm32 is None:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="STM32가 연결되어 있지 않습니다.",
                )

    if (
        stm32.current_theta1_deg is None
        or stm32.current_theta2_deg is None
        or stm32.current_theta3_deg is None
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="STM32 현재 각도 정보를 아직 받지 못했습니다.",
        )

    # SET_HOME은 위치를 움직이지 않으므로
    # 명령을 보내기 전에 현재 위치를 먼저 저장해 둔다.
    current_theta1 = stm32.current_theta1_deg
    current_theta2 = stm32.current_theta2_deg
    current_theta3 = stm32.current_theta3_deg

    success = stm32.set_home()

    if not success:
        if stm32.last_command_error_code is not None:
            return JSONResponse(
                status_code=409,
                content={
                    "success": False,
                    "error_code": stm32.last_command_error_code,
                    "error": stm32.last_command_error_name,
                },
            )

        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "error_code": None,
                "error": "STM32_SET_HOME_FAILED",
            },
        )

    with Session(engine) as session:
        statement = select(HomePosition).where(
            HomePosition.user_id == current_user.id
        )

        home_position = session.exec(statement).first()

        if home_position is None:
            home_position = HomePosition(
                user_id=current_user.id,
                theta1=current_theta1,
                theta2=current_theta2,
                theta3=current_theta3,
            )

        else:
            home_position.theta1 = current_theta1
            home_position.theta2 = current_theta2
            home_position.theta3 = current_theta3

        session.add(home_position)
        session.commit()
        session.refresh(home_position)

        return home_position





@app.get("/motor-setup")
def motor_setup_page():
    return FileResponse("motor_setup.html")



@app.get("/api/motor/position")
def get_motor_position(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효한 사용자가 아닙니다.",
        )

    stm32 = request.app.state.stm32

    if stm32 is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="STM32가 연결되어 있지 않습니다.",
        )

    if (
        stm32.current_theta1_deg is None
        or stm32.current_theta2_deg is None
        or stm32.current_theta3_deg is None
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="STM32 현재 각도 정보를 아직 받지 못했습니다.",
        )

    return {
        "theta1": round(stm32.current_theta1_deg, 1),
        "theta2": round(stm32.current_theta2_deg, 1),
        "theta3": round(stm32.current_theta3_deg, 1),
    }