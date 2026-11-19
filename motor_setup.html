<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스마트 모니터 암 - 모터 제어</title>
    <style>
        :root {
            --bg: #f5f3ed;
            --paper: #fffefa;
            --panel: #f6f7f3;
            --text: #27352e;
            --muted: #687970;
            --border: #dedfd6;
            --track: #e6e8e2;
            --accent: #547967;
            --accent-soft: #e7efe9;
            --plus: #b75b53;
            --plus-soft: #f8e8e4;
            --minus: #547e9d;
            --minus-soft: #e7eff5;
        }

        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: "Malgun Gothic", "Apple SD Gothic Neo", Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
        }
        button, input { font: inherit; }
        button {
            padding: 10px 14px;
            background: var(--paper);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 9px;
            cursor: pointer;
            transition: background .15s ease, border-color .15s ease;
        }
        button:hover:not(:disabled) { background: var(--accent-soft); }
        button:focus-visible, input:focus-visible {
            outline: 3px solid rgba(84, 121, 103, .28);
            outline-offset: 2px;
        }
        button:disabled { opacity: .48; cursor: not-allowed; }
        .page { max-width: 1210px; padding: 30px 24px 50px; margin: 0 auto; }
        h1 { font-size: 29px; margin: 0 0 8px; }
        .subtitle, .help { color: var(--muted); }
        .subtitle { margin: 0 0 24px; }
        .help { font-size: 13px; line-height: 1.6; }
        h2 { font-size: 20px; margin: 0 0 19px; }
        h3 { font-size: 15px; margin: 0 0 14px; }
        .card {
            background: var(--paper);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 14px rgba(36, 45, 37, .035);
        }
        .token-box { margin-bottom: 18px; }
        .token-box label { display: block; font-size: 14px; font-weight: bold; margin-bottom: 10px; }
        .token-box input {
            display: block; width: 100%; max-width: 730px;
            border: 1px solid #cbd2cb; border-radius: 9px;
            padding: 11px 12px; background: white;
        }
        .main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
        .angle-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }
        .angle-item { text-align: center; }
        .angle-item h3 { margin: 8px 0 18px; }
        .angle-circle {
            margin: auto; width: 132px; height: 132px; border-radius: 50%;
            background: var(--track);
            position: relative; display: grid; place-items: center;
        }
        .angle-circle::before {
            content: ""; position: absolute; inset: 9px;
            border-radius: 50%; background: var(--paper);
        }
        .angle-circle .value {
            position: relative; z-index: 1;
            font-size: 24px; font-weight: bold; white-space: nowrap;
        }
        .angle-guide { margin: 14px 0 0; text-align: center; font-size: 12px; color: var(--muted); }
        .axis-quick-grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 10px; }
        .quick-card { text-align: center; padding: 15px 8px; border-radius: 11px; background: var(--panel); }
        .quick-card h3 { margin-bottom: 11px; }
        .quick-actions { display: flex; justify-content: center; flex-wrap: wrap; gap: 7px; }
        .quick-actions button { min-width: 45px; font-size: 20px; font-weight: bold; }
        .quick-actions button:first-child { color: var(--minus); }
        .quick-actions button:last-child { color: var(--plus); }
        .separator { border: 0; border-top: 1px solid var(--border); margin: 22px 0; }
        .preset-heading { font-weight: bold; margin-bottom: 10px; }
        .choice-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 13px; align-items: center; }
        .choice-label { min-width: 65px; font-size: 14px; color: var(--muted); }
        .choice-row button { min-width: 58px; }
        .axis-choice.selected {
            color: var(--accent); background: var(--accent-soft); border-color: var(--accent);
        }
        /* Direction and degree controls share one horizontal row. */
        .preset-option-row {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 10px;
        }
        .preset-option-group { min-width: 0; }
        .preset-option-title {
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: var(--muted);
            margin-bottom: 10px;
        }
        .preset-buttons {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .preset-buttons .direction-choice { min-width: 75px; }
        .preset-buttons .degree-choice { min-width: 55px; }
        .preset-short-divider {
            display: block;
            height: 42px;
            width: 1px;
            flex: 0 0 1px;
            background: var(--border);
            align-self: center;
        }
        .preset-cancel-row { display: flex; justify-content: flex-end; margin-bottom: 10px; }
        .direction-choice { font-weight: bold; }
        .direction-choice.selected-positive, .degree-choice.positive {
            color: var(--plus); background: var(--plus-soft); border-color: var(--plus);
        }
        .direction-choice.selected-negative, .degree-choice.negative {
            color: var(--minus); background: var(--minus-soft); border-color: var(--minus);
        }
        .direction-choice.selected-positive:hover:not(:disabled), .degree-choice.positive:hover:not(:disabled) { background: #f4dbd5; }
        .direction-choice.selected-negative:hover:not(:disabled), .degree-choice.negative:hover:not(:disabled) { background: #d6e6f1; }
        .cancel-button { color: #8d594b; }
        .saved-section { margin-top: 18px; }
        .saved-grid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 12px; margin-bottom: 17px; }
        .saved-card {
            padding: 18px; border: 1px solid var(--border); border-radius: 11px;
            min-height: 130px; background: var(--paper);
        }
        .saved-card h3 { font-size: 17px; margin-bottom: 21px; }
        .home-card { background: var(--accent-soft); border-color: #bed2c4; }
        .home-button { background: var(--accent); border-color: var(--accent); color: white; }
        .home-button:hover:not(:disabled) { background: #426a57; }
        .status-box { margin: 18px 0 0; padding: 15px 17px; border-radius: 10px; background: var(--accent-soft); color: #3c6550; line-height: 1.6; }
        .status-box[data-tone="working"] { background: #fff2df; color: #7c5a2b; }
        .status-box[data-tone="error"] { background: #fae8e5; color: #993d35; }
        .status-box[data-tone="success"] { background: #e4f1e8; color: #2d6f4b; }
        .log-card { margin-top: 18px; }
        .log-box {
            border-radius: 10px; background: #242b27; color: #e9eee9;
            padding: 16px; max-height: 250px; min-height: 105px;
            overflow: auto; font: 13px/1.7 Consolas, "Courier New", monospace;
        }
        .log-line { white-space: pre-wrap; overflow-wrap: anywhere; }
        .log-line.tx { color: #9fd1b4; }
        .log-line.rx { color: #bdd2e2; }
        .log-line.err { color: #ffb3a5; }
        .log-line.done { color: #f4d6a2; }
        .footnote { font-size: 12px; color: var(--muted); margin: 9px 0 0; line-height: 1.6; }
        @media (max-width: 940px) {
            .main-grid { grid-template-columns: 1fr; }
        }
        @media (max-width: 640px) {
            .page { padding: 22px 12px 35px; }
            .card { padding: 17px 12px; }
            .saved-grid { grid-template-columns: repeat(2, minmax(0,1fr)); }
            .angle-circle { width: 96px; height: 96px; }
            .angle-circle .value { font-size: 17px; }
            .angle-item h3 { font-size: 12px; }
            .quick-actions button { min-width: 38px; }
            .preset-option-row { flex-wrap: wrap; gap: 10px; }
            .preset-short-divider { height: 36px; }
        }
    </style>
</head>
<body>
<div class="page">
    <h1>스마트 모니터 암</h1>

    <section class="card token-box">
        <label for="token">JWT Access Token</label>
        <input id="token" type="password" placeholder="Swagger에서 발급받은 access_token" autocomplete="off">
    </section>

    <div class="main-grid">
        <section class="card">
            <h2>현재 각도</h2>
            <div class="angle-grid">
                <div class="angle-item">
                    <h3>θ1 </h3>
                    <div class="angle-circle" id="circle1"><span class="value"><span id="theta1">--</span>°</span></div>
                </div>
                <div class="angle-item">
                    <h3>θ2 </h3>
                    <div class="angle-circle" id="circle2"><span class="value"><span id="theta2">--</span>°</span></div>
                </div>
                <div class="angle-item">
                    <h3>θ3 </h3>
                    <div class="angle-circle" id="circle3"><span class="value"><span id="theta3">--</span>°</span></div>
                </div>
            </div>
        </section>

        <section class="card">
            <h2>수동 제어</h2>
            <div class="axis-quick-grid">
                <div class="quick-card">
                    <h3>θ1</h3>
                    <div class="quick-actions">
                        <button class="action-button" type="button" onclick="jog(1, -1.0)" aria-label="θ1 마이너스 1도">−</button>
                        <button class="action-button" type="button" onclick="jog(1, 1.0)" aria-label="θ1 플러스 1도">+</button>
                    </div>
                </div>
                <div class="quick-card">
                    <h3>θ2</h3>
                    <div class="quick-actions">
                        <button class="action-button" type="button" onclick="jog(2, -1.0)" aria-label="θ2 마이너스 1도">−</button>
                        <button class="action-button" type="button" onclick="jog(2, 1.0)" aria-label="θ2 플러스 1도">+</button>
                    </div>
                </div>
                <div class="quick-card">
                    <h3>θ3</h3>
                    <div class="quick-actions">
                        <button class="action-button" type="button" onclick="jog(3, -1.0)" aria-label="θ3 마이너스 1도">−</button>
                        <button class="action-button" type="button" onclick="jog(3, 1.0)" aria-label="θ3 플러스 1도">+</button>
                    </div>
                </div>
            </div>

            <hr class="separator">
            <p class="preset-heading">각도 선택 이동</p>
            <div class="choice-row">
                <span class="choice-label">축 선택</span>
                <button type="button" class="axis-choice" data-axis="1" onclick="chooseAxis(1)">θ1</button>
                <button type="button" class="axis-choice" data-axis="2" onclick="chooseAxis(2)">θ2</button>
                <button type="button" class="axis-choice" data-axis="3" onclick="chooseAxis(3)">θ3</button>
            </div>
            <div class="preset-option-row">
                <div class="preset-option-group">
                    <span class="preset-option-title">② 방향 선택</span>
                    <div class="preset-buttons">
                        <button type="button" class="direction-choice" data-direction="-1" onclick="chooseDirection(-1)">− 방향</button>
                        <button type="button" class="direction-choice" data-direction="1" onclick="chooseDirection(1)">+ 방향</button>
                    </div>
                </div>

                <span class="preset-short-divider" aria-hidden="true"></span>

                <div class="preset-option-group">
                    <span class="preset-option-title">③ 이동 각도 선택</span>
                    <div class="preset-buttons">
                        <button type="button" class="degree-choice" onclick="runPreset(5)" disabled>5°</button>
                        <button type="button" class="degree-choice" onclick="runPreset(10)" disabled>10°</button>
                        <button type="button" class="degree-choice" onclick="runPreset(20)" disabled>20°</button>
                    </div>
                </div>
            </div>
            <div class="preset-cancel-row">
                <button id="cancel-preset" class="cancel-button" type="button" onclick="cancelPreset()" disabled>추가 명령 중단</button>
            </div>
        </section>
    </div>

    <section class="card saved-section">
        <h2>저장된 위치</h2>
        <div class="saved-grid">
            <div class="saved-card home-card">
                <h3>HOME</h3>
                <button type="button" class="action-button" onclick="moveHome()">▶ 이동</button>
            </div>
            <div class="saved-card">
                <h3>문서 작업</h3>
                <button type="button" disabled>이동</button>
            </div>
            <div class="saved-card">
                <h3>영상 시청</h3>
                <button type="button" disabled>이동</button>
            </div>
            <div class="saved-card">
                <h3>＋ 새 위치 저장</h3>
                <button type="button" disabled>추가</button>
            </div>
        </div>
        <button type="button" class="home-button action-button" onclick="saveHome()">현재 위치를 HOME으로 저장</button>
    </section>

    <p id="status" class="status-box" role="status" aria-live="polite">상태: JWT 입력을 기다리는 중입니다.</p>

    <section class="card log-card">
        <h2>모터 제어 로그</h2>
        <div id="command-log" class="log-box" role="log" aria-live="off">
            <div class="log-line">[READY]</div>
        </div>
    </section>
</div>

<script>
    let theta1 = null;
    let theta2 = null;
    let theta3 = null;

    let selectedAxis = 1;
    let selectedDirection = null;
    let isBusy = false;
    let isPresetRunning = false;
    let stopAfterCurrent = false;

    function getToken() {
        return document.getElementById("token").value.trim();
    }

    function setStatus(message, tone = "normal") {
        const element = document.getElementById("status");
        element.textContent = "상태: " + message;
        element.dataset.tone = tone;
    }

    function appendLog(kind, message) {
        const log = document.getElementById("command-log");
        const now = new Date().toLocaleTimeString("ko-KR", { hour12: false });
        const line = document.createElement("div");
        line.className = "log-line " + kind;
        line.textContent = `[${now}] [${kind.toUpperCase()}] ${message}`;
        log.appendChild(line);
        while (log.children.length > 140) {
            log.removeChild(log.firstChild);
        }
        log.scrollTop = log.scrollHeight;
    }

    function axisName(axis) {
        return "θ" + axis;
    }

    function directionName(delta) {
        return delta > 0 ? "+ 방향" : "− 방향";
    }

    function renderAngle(axis, value) {
        document.getElementById("theta" + axis).textContent = value.toFixed(1);
        const circle = document.getElementById("circle" + axis);
        const amount = Math.min(Math.abs(value), 360);

        if (amount < 0.00001) {
            circle.style.background = "var(--track)";
        } else if (value > 0) {
            circle.style.background =
                `conic-gradient(var(--plus) 0deg ${amount}deg, var(--track) ${amount}deg 360deg)`;
        } else {
            circle.style.background =
                `conic-gradient(from ${360 - amount}deg, var(--minus) 0deg ${amount}deg, var(--track) ${amount}deg 360deg)`;
        }
    }

    function refreshControlUI() {
        document.querySelectorAll(".axis-choice").forEach(button => {
            button.classList.toggle("selected", Number(button.dataset.axis) === selectedAxis);
            button.disabled = isBusy;
        });
        document.querySelectorAll(".direction-choice").forEach(button => {
            const direction = Number(button.dataset.direction);
            button.classList.toggle("selected-positive", direction === selectedDirection && direction > 0);
            button.classList.toggle("selected-negative", direction === selectedDirection && direction < 0);
            button.disabled = isBusy;
        });
        document.querySelectorAll(".degree-choice").forEach(button => {
            const ready = selectedDirection !== null;
            button.classList.toggle("positive", ready && selectedDirection > 0);
            button.classList.toggle("negative", ready && selectedDirection < 0);
            button.disabled = isBusy || !ready;
        });
        document.querySelectorAll(".action-button").forEach(button => {
            button.disabled = isBusy;
        });
        document.getElementById("cancel-preset").disabled = !isPresetRunning;
    }

    function chooseAxis(axis) {
        if (isBusy || ![1, 2, 3].includes(axis)) return;
        selectedAxis = axis;
        refreshControlUI();
        setStatus(`${axisName(axis)} 선택됨. 방향을 선택한 뒤 이동 각도를 누르세요.`);
    }

    function chooseDirection(direction) {
        if (isBusy || ![-1, 1].includes(direction)) return;
        selectedDirection = direction;
        refreshControlUI();
        setStatus(`${axisName(selectedAxis)} / ${directionName(direction)} 선택됨. 5°, 10°, 20° 중 하나를 누르세요.`);
    }

    async function refreshMotorPosition(quiet = false) {
        const token = getToken();
        if (!token) {
            if (!quiet) setStatus("JWT를 먼저 입력해주세요.", "error");
            return false;
        }
        try {
            const response = await fetch("/api/motor/position", {
                method: "GET",
                headers: { "Authorization": "Bearer " + token }
            });
            if (!response.ok) throw new Error(`현재 각도 조회 실패 (HTTP ${response.status})`);
            const result = await response.json();
            if (![result.theta1, result.theta2, result.theta3].every(value =>
                typeof value === "number" && Number.isFinite(value))) {
                throw new Error("현재 각도 응답 형식이 올바르지 않습니다.");
            }
            theta1 = result.theta1;
            theta2 = result.theta2;
            theta3 = result.theta3;
            renderAngle(1, theta1);
            renderAngle(2, theta2);
            renderAngle(3, theta3);
            if (!quiet) {
                setStatus("현재 명령 각도 조회 완료", "success");
                appendLog("rx", `현재 명령각 θ1=${theta1.toFixed(1)}° / θ2=${theta2.toFixed(1)}° / θ3=${theta3.toFixed(1)}°`);
            }
            return true;
        } catch (error) {
            setStatus(error.message || "현재 각도 조회 오류", "error");
            appendLog("err", error.message || "현재 각도 조회 오류");
            return false;
        }
    }

    async function sendOneDegree(axis, direction) {
        const token = getToken();
        if (!token) throw new Error("JWT를 먼저 입력해주세요.");
        if (![1, 2, 3].includes(axis) || ![-1, 1].includes(direction)) {
            throw new Error("잘못된 축 또는 방향 값입니다.");
        }
        const deltaDeg = direction * 1.0;
        appendLog("tx", `${axisName(axis)} ${directionName(direction)} 1° JOG → POST /api/motor/jog`);
        const response = await fetch("/api/motor/jog", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ axis: axis, delta_deg: deltaDeg })
        });
        if (!response.ok) {
            throw new Error(`JOG 실패 (HTTP ${response.status})`);
        }
        await response.json();
        appendLog("rx", `JOG 정상 응답 (HTTP ${response.status})`);
    }

    async function jog(axis, deltaDeg) {
        if (isBusy) return;
        if (!getToken()) {
            setStatus("JWT를 먼저 입력해주세요.", "error");
            return;
        }
        if (![1, 2, 3].includes(axis) || ![-1, 1].includes(deltaDeg)) return;
        isBusy = true;
        refreshControlUI();
        try {
            setStatus(`${axisName(axis)} ${directionName(deltaDeg)} 1° 회전 명령 처리 중`, "working");
            await sendOneDegree(axis, deltaDeg);
            const ok = await refreshMotorPosition(true);
            if (!ok) throw new Error("각도 갱신을 확인하지 못했습니다.");
            setStatus(`${axisName(axis)} ${directionName(deltaDeg)} 1° JOG 처리 완료 (명령각 갱신 확인)`, "success");
            appendLog("done", `${axisName(axis)} ${directionName(deltaDeg)} 1° 명령 처리 완료`);
        } catch (error) {
            setStatus(error.message || "JOG 통신 오류", "error");
            appendLog("err", error.message || "JOG 통신 오류");
        } finally {
            isBusy = false;
            refreshControlUI();
        }
    }

    function cancelPreset() {
        if (!isPresetRunning) return;
        stopAfterCurrent = true;
        setStatus("연속 JOG 중단 요청: 현재 전송 중인 명령 처리 후 추가 요청을 보내지 않습니다.", "working");
        appendLog("err", "사용자가 연속 JOG 추가 전송 중단을 요청했습니다.");
    }

    async function runPreset(degrees) {
        if (isBusy || ![5, 10, 20].includes(degrees) || selectedDirection === null) return;
        if (!getToken()) {
            setStatus("JWT를 먼저 입력해주세요.", "error");
            return;
        }
        const axis = selectedAxis;
        const direction = selectedDirection;
        const approved = window.confirm(
            `${axisName(axis)} ${directionName(direction)} ${degrees}° 이동을 1° JOG ${degrees}회로 순차 요청합니다.\n` +
            "먼저 시뮬레이터에서 시험하고, 실제 장비의 안전 범위를 확인하세요. 계속할까요?"
        );
        if (!approved) return;

        isBusy = true;
        isPresetRunning = true;
        stopAfterCurrent = false;
        refreshControlUI();
        let completed = 0;
        try {
            appendLog("tx", `${axisName(axis)} ${directionName(direction)} ${degrees}° 회전 명령 시작 (${degrees} × 1° JOG)`);
            for (let n = 1; n <= degrees; n++) {
                if (stopAfterCurrent) break;
                setStatus(`${axisName(axis)} ${directionName(direction)} ${degrees}° 회전 명령 처리 중 (${n}/${degrees})`, "working");
                await sendOneDegree(axis, direction);
                completed++;
                const ok = await refreshMotorPosition(true);
                if (!ok) throw new Error("각도 조회 실패로 연속 JOG를 중단했습니다.");
            }
            if (stopAfterCurrent) {
                setStatus(`${axisName(axis)} 연속 JOG 중단됨: ${degrees}회 중 ${completed}회 응답 확인`, "working");
                appendLog("done", `중단됨: ${completed}/${degrees}회 처리`);
            } else {
                setStatus(`${axisName(axis)} ${directionName(direction)} ${degrees}° JOG 요청 처리 완료 (${completed}회 응답 확인)`, "success");
                appendLog("done", `${axisName(axis)} ${directionName(direction)} ${degrees}° 명령 처리 완료 / 현재 명령각 반영`);
            }
        } catch (error) {
            setStatus(`${completed}/${degrees}회 진행 후 중단: ${error.message}`, "error");
            appendLog("err", `${completed}/${degrees}회 후 실패: ${error.message}`);
        } finally {
            isBusy = false;
            isPresetRunning = false;
            stopAfterCurrent = false;
            refreshControlUI();
        }
    }

    async function saveHome() {
        if (isBusy) return;
        if (!getToken()) {
            setStatus("JWT를 먼저 입력해주세요.", "error");
            return;
        }
        isBusy = true;
        refreshControlUI();
        try {
            setStatus("현재 위치를 HOME으로 저장 요청 중", "working");
            appendLog("tx", "HOME 저장 → POST /api/home/save");
            const response = await fetch("/api/home/save", {
                method: "POST",
                headers: { "Authorization": "Bearer " + getToken() }
            });
            if (!response.ok) throw new Error(`HOME 저장 실패 (HTTP ${response.status})`);
            await response.json();
            appendLog("rx", `HOME 저장 요청 정상 응답 (HTTP ${response.status})`);
            await refreshMotorPosition(true);
            setStatus("현재 위치를 HOME으로 저장했습니다. HOME 변경 후 기준 자세 재캘리브레이션이 필요합니다.", "success");
            appendLog("done", "HOME 저장 처리 완료");
        } catch (error) {
            setStatus(error.message || "HOME 저장 통신 오류", "error");
            appendLog("err", error.message || "HOME 저장 통신 오류");
        } finally {
            isBusy = false;
            refreshControlUI();
        }
    }

    async function moveHome() {
        if (isBusy) return;
        if (!getToken()) {
            setStatus("JWT를 먼저 입력해주세요.", "error");
            return;
        }
        isBusy = true;
        refreshControlUI();
        try {
            setStatus("저장된 HOME으로 이동 명령 처리 중", "working");
            appendLog("tx", "HOME으로 이동 → POST /api/motor/move-home");
            const response = await fetch("/api/motor/move-home", {
                method: "POST",
                headers: { "Authorization": "Bearer " + getToken() }
            });
            if (!response.ok) throw new Error(`HOME 이동 실패 (HTTP ${response.status})`);
            await response.json();
            appendLog("rx", `HOME 이동 요청 정상 응답 (HTTP ${response.status})`);
            const ok = await refreshMotorPosition(true);
            if (!ok) throw new Error("HOME 명령은 응답했으나 현재 각도 조회에 실패했습니다.");
            setStatus("HOME 복귀 명령 처리 완료 (현재 명령각 확인)", "success");
            appendLog("done", "HOME 이동 명령 처리 완료");
        } catch (error) {
            setStatus(error.message || "HOME 이동 통신 오류", "error");
            appendLog("err", error.message || "HOME 이동 통신 오류");
        } finally {
            isBusy = false;
            refreshControlUI();
        }
    }

    document.getElementById("token").addEventListener("change", async function () {
        if (getToken()) await refreshMotorPosition();
    });

    refreshControlUI();
</script>
</body>
</html>
