document.addEventListener('DOMContentLoaded', function () {
    const startBtn = document.querySelector('.start-btn');
    const resetBtn = document.querySelector('.reset-btn');
    const timerTime = document.querySelector('.timer-time');
    const timerLabel = document.querySelector('.timer-label');
    const progressCircle = document.querySelectorAll('svg circle')[1];

    let timer = null;
    let totalSeconds = 25 * 60;
    let remainingSeconds = totalSeconds;
    let isRunning = false;
    let completedCount = 0;
    let totalFocusSeconds = 0;
    const progressNum = document.querySelector('.progress-done .progress-num');
    const progressTime = document.querySelector('.progress-time .progress-num');

    function updateDisplay() {
        const min = String(Math.floor(remainingSeconds / 60)).padStart(2, '0');
        const sec = String(remainingSeconds % 60).padStart(2, '0');
        timerTime.textContent = `${min}:${sec}`;
        // 円形プログレスバーの更新
        const percent = 1 - (remainingSeconds / totalSeconds);
        const dashoffset = 502 * (1 - percent);
        progressCircle.setAttribute('stroke-dashoffset', dashoffset);
    }

    function startTimer() {
        if (isRunning) return;
        isRunning = true;
        timerLabel.textContent = '作業中';
        timer = setInterval(() => {
            if (remainingSeconds > 0) {
                remainingSeconds--;
                updateDisplay();
            } else {
                clearInterval(timer);
                isRunning = false;
                timerLabel.textContent = '終了！';
                completedCount++;
                totalFocusSeconds += totalSeconds;
                updateProgress();
                alert('ポモドーロ終了！お疲れさまです。');
            }
        }, 1000);
    }

    function resetTimer() {
        clearInterval(timer);
        isRunning = false;
        remainingSeconds = totalSeconds;
        timerLabel.textContent = '作業中';
        updateDisplay();
    }

    function updateProgress() {
        progressNum.textContent = completedCount;
        // 分単位で表示（例：1時間40分）
        const hours = Math.floor(totalFocusSeconds / 3600);
        const minutes = Math.floor((totalFocusSeconds % 3600) / 60);
        let timeStr = '';
        if (hours > 0) {
            timeStr += hours + '時間';
        }
        timeStr += minutes + '分';
        progressTime.textContent = timeStr;
    }

    startBtn.addEventListener('click', startTimer);
    resetBtn.addEventListener('click', resetTimer);

    // 初期表示
    updateDisplay();
    updateProgress();
});
