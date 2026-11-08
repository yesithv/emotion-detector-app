const EMOTIONS = ["anger", "disgust", "fear", "joy", "sadness"];

const EMOJIS = {
    anger: "😠",
    disgust: "🤢",
    fear: "😨",
    joy: "😄",
    sadness: "😢"
};


async function RunEmotionDetection() {
    const textArea = document.getElementById("textToAnalyze");
    const analyzeButton = document.getElementById("analyzeButton");

    const textToAnalyze = textArea.value.trim();

    if (!textToAnalyze) {
        showError("Invalid text! Please try again!");
        return;
    }

    analyzeButton.disabled = true;
    analyzeButton.textContent = "Detecting...";

    try {
        const response = await fetch(
            `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to analyze the text.");
        }

        showResult(data);

    } catch (error) {
        showError(error.message);
    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Detect Emotions";
    }
}


function showResult(data) {
    const dominantEmotion = document.getElementById("dominantEmotion");
    const emotionScores = document.getElementById("emotionScores");

    dominantEmotion.textContent =
        `${EMOJIS[data.dominant_emotion]} ${data.dominant_emotion.toUpperCase()}`;
    dominantEmotion.className = `dominant-emotion ${data.dominant_emotion}`;

    emotionScores.replaceChildren(
        ...EMOTIONS.map((emotion) => buildScoreRow(
            emotion,
            data[emotion],
            emotion === data.dominant_emotion
        ))
    );

    document.getElementById("errorMessage").classList.add("hidden");
    emotionScores.classList.remove("hidden");
    showResultContent();
}


function buildScoreRow(emotion, score, isDominant) {
    const percentage = (score * 100).toFixed(2);

    const row = document.createElement("li");
    row.className = isDominant ? "score-row dominant" : "score-row";

    const name = document.createElement("span");
    name.className = "score-name";
    name.textContent = emotion;

    const bar = document.createElement("div");
    bar.className = "score-bar";

    const fill = document.createElement("div");
    fill.className = `score-fill ${emotion}`;
    fill.style.width = `${percentage}%`;
    bar.appendChild(fill);

    const value = document.createElement("span");
    value.className = "score-value";
    value.textContent = `${percentage}%`;

    row.append(name, bar, value);
    return row;
}


function showError(message) {
    const dominantEmotion = document.getElementById("dominantEmotion");
    const errorMessage = document.getElementById("errorMessage");

    dominantEmotion.textContent = "ERROR";
    dominantEmotion.className = "dominant-emotion error";

    errorMessage.textContent = message;
    errorMessage.classList.remove("hidden");

    document.getElementById("emotionScores").classList.add("hidden");
    showResultContent();
}


function showResultContent() {
    document.getElementById("emptyState").classList.add("hidden");
    document.getElementById("resultContent").classList.remove("hidden");
}
