import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nile & Pyramids - Egypt RAG Assistant",
    page_icon="🏺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HIDE STREAMLIT UI
# ============================================================

st.markdown(
    """
    <style>
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        .stApp {
            margin: 0 !important;
            padding: 0 !important;
        }

        .main {
            padding: 0 !important;
        }

        .block-container {
            padding: 0 !important;
            max-width: none !important;
        }

        [data-testid="stAppViewContainer"] {
            padding: 0 !important;
        }

        [data-testid="stHeader"] {
            display: none;
        }

        iframe {
            border: none !important;
            width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# EXACT HTML UI
# ============================================================

html = r"""
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8" />

    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>Nile & Pyramids - Egypt RAG Assistant</title>

    <link rel="preconnect" href="https://fonts.googleapis.com" />

    <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossorigin
    />

    <link
        href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap"
        rel="stylesheet"
    />

    <style>

        :root {
            --bg: #f5ead7;
            --surface: #fff9ed;
            --surface-2: #f8efdf;
            --border: #c9a66b;
            --border-light: #dec69e;
            --gold: #9a6b35;
            --gold-bright: #68451f;
            --text: #463524;
            --muted: #967850;
            --ink: #68451f;
            --green: #5a8a6a;
            --red: #c45a5a;
            --radius: 16px;
        }


        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }


        html,
        body {
            width: 100%;
            min-height: 100%;
        }


        body {
            min-height: 100vh;
            color: var(--text);
            font-family: "DM Sans", sans-serif;

            background:
                radial-gradient(
                    circle at 12% 5%,
                    rgba(201, 166, 107, .25),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 88% 12%,
                    rgba(219, 186, 125, .22),
                    transparent 28%
                ),
                var(--bg);
        }


        .app {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }


        /* =====================================================
           TOPBAR
           ===================================================== */

        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;

            min-height: 72px;

            padding: 12px 32px;

            border-bottom: 1px solid var(--border-light);

            background: rgba(245, 234, 215, .85);

            backdrop-filter: blur(12px);
        }


        .brand {
            display: flex;
            align-items: center;
            gap: 14px;

            min-width: max-content;
        }


        .crest {
            display: grid;
            place-items: center;

            width: 42px;
            height: 42px;

            border: 1px solid var(--gold);
            border-radius: 50%;

            color: var(--gold-bright);

            background: rgba(154, 107, 53, .12);

            font-size: 1.3rem;
        }


        .brand h1 {
            font:
                700 1.3rem
                "Playfair Display",
                serif;

            color: var(--gold-bright);

            letter-spacing: .2px;
        }


        .brand p {
            margin-top: 2px;

            color: var(--muted);

            font-size: .72rem;
        }


        /* =====================================================
           CONNECTION
           ===================================================== */

        .connection {
            display: flex;
            align-items: center;
            gap: 10px;
        }


        .connection input {
            width: 245px;

            border: 1px solid var(--border);

            border-radius: 9px;

            padding: 9px 11px;

            outline: none;

            color: var(--ink);

            background: var(--surface);

            font: .82rem "DM Sans", sans-serif;
        }


        .connection input:focus {
            border-color: var(--gold);

            box-shadow:
                0 0 0 2px
                rgba(154, 107, 53, .12);
        }


        button {
            border: 0;

            border-radius: 9px;

            padding: 10px 14px;

            cursor: pointer;

            font:
                600 .82rem
                "DM Sans",
                sans-serif;

            transition:
                transform .15s,
                border-color .15s,
                background .15s,
                box-shadow .15s;
        }


        button:hover {
            transform: translateY(-1px);
        }


        button:disabled {
            opacity: .55;

            cursor: wait;

            transform: none;
        }


        .ping {
            border: 1px solid var(--border);

            color: var(--gold-bright);

            background: var(--surface);
        }


        .ping:hover {
            border-color: var(--gold);

            background: var(--surface-2);
        }


        .dot {
            width: 10px;
            height: 10px;

            border-radius: 50%;

            background: #b0a090;
        }


        .dot.idle {
            background: #b0a090;
        }


        .dot.ok {
            background: var(--green);

            box-shadow:
                0 0 0 4px
                rgba(90, 138, 106, .14);
        }


        .dot.error {
            background: var(--red);

            box-shadow:
                0 0 0 4px
                rgba(196, 90, 90, .14);
        }


        /* =====================================================
           WORKSPACE
           ===================================================== */

        .workspace {
            flex: 1;

            display: grid;

            grid-template-columns:
                minmax(310px, .9fr)
                minmax(380px, 1.1fr);

            gap: 20px;

            width:
                min(
                    1200px,
                    calc(100% - 48px)
                );

            margin: 0 auto;

            padding: 28px 0;
        }


        .panel {
            min-height: 520px;

            overflow: hidden;

            border:
                1px solid
                var(--border-light);

            border-radius: var(--radius);

            background: var(--surface);

            box-shadow:
                0 10px 30px
                rgba(93, 67, 38, .08);
        }


        /* =====================================================
           INPUT PANEL
           ===================================================== */

        .input-panel {
            display: flex;

            flex-direction: column;

            padding: 24px;
        }


        .panel-heading {
            display: flex;

            align-items: center;

            justify-content: space-between;

            margin-bottom: 16px;
        }


        .eyebrow {
            color: var(--gold);

            font-size: .7rem;

            font-weight: 700;

            letter-spacing: .12em;

            text-transform: uppercase;
        }


        .hint {
            color: var(--muted);

            font-size: .75rem;
        }


        .input-panel h2 {
            font:
                700 1.75rem
                "Playfair Display",
                serif;

            color: var(--gold-bright);
        }


        .input-panel > p {
            margin: 10px 0 20px;

            color: var(--muted);

            line-height: 1.55;

            font-size: .9rem;
        }


        textarea {
            flex: 1;

            width: 100%;

            min-height: 200px;

            border:
                1px solid
                var(--border-light);

            border-radius: 12px;

            padding: 15px;

            resize: none;

            outline: none;

            color: var(--text);

            background: var(--surface-2);

            font:
                .95rem/1.6
                "DM Sans",
                sans-serif;
        }


        textarea:focus {
            border-color: var(--gold);

            box-shadow:
                0 0 0 3px
                rgba(154, 107, 53, .1);
        }


        textarea::placeholder {
            color: var(--muted);
        }


        /* =====================================================
           ASK BUTTON
           ===================================================== */

        .ask-button {
            margin-top: 14px;

            padding: 14px;

            color: #fff8e9;

            background:
                linear-gradient(
                    135deg,
                    var(--gold),
                    var(--gold-bright)
                );

            font-size: .92rem;
        }


        .ask-button:hover {
            box-shadow:
                0 7px 20px
                rgba(154, 107, 53, .25);
        }


        /* =====================================================
           EXAMPLES
           ===================================================== */

        .examples {
            margin-top: 20px;
        }


        .examples p {
            margin-bottom: 9px;

            color: var(--muted);

            font-size: .75rem;
        }


        .chips {
            display: flex;

            flex-wrap: wrap;

            gap: 7px;
        }


        .chip {
            padding: 7px 10px;

            border:
                1px solid
                var(--border-light);

            border-radius: 8px;

            color: var(--muted);

            background: var(--surface-2);

            font-size: .72rem;

            font-weight: 500;
        }


        .chip:hover {
            border-color: var(--gold);

            color: var(--gold-bright);
        }


        /* =====================================================
           RESULT PANEL
           ===================================================== */

        .result-panel {
            display: flex;

            flex-direction: column;
        }


        .result-title {
            display: flex;

            justify-content: space-between;

            align-items: center;

            padding:
                24px
                24px
                18px;

            border-bottom:
                1px solid
                var(--border-light);
        }


        .result-title h2 {
            font:
                700 1.75rem
                "Playfair Display",
                serif;

            color: var(--gold-bright);
        }


        .status-text {
            color: var(--muted);

            font-size: .75rem;
        }


        .result-body {
            flex: 1;

            padding: 24px;

            overflow-y: auto;
        }


        .empty-state {
            height: 100%;

            display: grid;

            place-content: center;

            gap: 10px;

            text-align: center;

            color: var(--muted);
        }


        .empty-icon {
            font-size: 3rem;

            opacity: .6;
        }


        .empty-state h3 {
            color: var(--gold-bright);

            font:
                600 1.15rem
                "Playfair Display",
                serif;
        }


        .empty-state p {
            max-width: 250px;

            font-size: .85rem;

            line-height: 1.5;
        }


        .answer {
            display: none;

            animation:
                rise .35s ease both;
        }


        .answer-question {
            margin-bottom: 16px;

            color: var(--gold);

            font-size: .85rem;

            line-height: 1.5;

            font-style: italic;
        }


        .answer-box {
            padding: 18px;

            border:
                1px solid
                var(--border-light);

            border-radius: 12px;

            color: var(--ink);

            background: var(--surface-2);

            line-height: 1.65;

            white-space: pre-wrap;
        }


        .sources {
            margin-top: 22px;
        }


        .sources h3 {
            margin-bottom: 10px;

            color: var(--gold);

            font-size: .75rem;

            letter-spacing: .1em;

            text-transform: uppercase;
        }


        .source {
            display: flex;

            align-items: center;

            gap: 10px;

            margin-top: 8px;

            padding: 10px 12px;

            border-radius: 9px;

            background: var(--surface);

            border:
                1px solid
                var(--border-light);

            color: var(--text);

            font-size: .82rem;
        }


        .page-number {
            min-width: 30px;

            color: var(--gold-bright);

            font-weight: 700;
        }


        /* =====================================================
           ERROR
           ===================================================== */

        .error-bar {
            display: none;

            width:
                min(
                    1200px,
                    calc(100% - 48px)
                );

            margin:
                -12px auto
                24px;

            padding: 12px 15px;

            border:
                1px solid
                rgba(196, 90, 90, .4);

            border-radius: 10px;

            color: var(--red);

            background:
                rgba(196, 90, 90, .1);

            font-size: .85rem;
        }


        .error-bar.show {
            display: block;
        }


        /* =====================================================
           ANIMATION
           ===================================================== */

        @keyframes rise {

            from {
                opacity: 0;

                transform:
                    translateY(8px);
            }

            to {
                opacity: 1;

                transform:
                    translateY(0);
            }

        }


        /* =====================================================
           RESPONSIVE
           ===================================================== */

        @media (max-width: 800px) {

            .topbar {
                align-items: flex-start;

                flex-direction: column;

                padding:
                    16px 20px;
            }


            .connection {
                width: 100%;
            }


            .connection input {
                flex: 1;

                width: auto;
            }


            .workspace {
                grid-template-columns: 1fr;

                width:
                    min(
                        calc(100% - 28px),
                        680px
                    );

                padding:
                    18px 0;
            }


            .panel {
                min-height: auto;
            }


            .input-panel {
                min-height: 440px;
            }


            .result-panel {
                min-height: 420px;
            }


            .error-bar {
                width:
                    min(
                        calc(100% - 28px),
                        680px
                    );
            }

        }

    </style>

</head>


<body>

<div class="app">


    <!-- =====================================================
         TOPBAR
         ===================================================== -->

    <header class="topbar">

        <div class="brand">

            <div class="crest">
                🏺
            </div>

            <div>

                <h1>
                    Nile &amp; Pyramids
                </h1>

                <p>
                    Your little Egypt travel companion
                </p>

            </div>

        </div>


        <div class="connection">

            <input
                id="api-url"
                value="http://localhost:8000"
                aria-label="FastAPI URL"
            />

            <button
                id="health-button"
                class="ping"
                type="button"
            >
                Ping API
            </button>

            <span
                id="health-dot"
                class="dot idle"
                title="API status"
            ></span>

        </div>

    </header>


    <!-- =====================================================
         WORKSPACE
         ===================================================== -->

    <main class="workspace">


        <!-- =================================================
             LEFT PANEL
             ================================================= -->

        <section class="panel input-panel">

            <div class="panel-heading">

                <span class="eyebrow">
                    Ask the guide
                </span>

                <span class="hint">
                    Ctrl + Enter to search
                </span>

            </div>


            <h2>
                Your question
            </h2>


            <p>
                Search the Lonely Planet Egypt guide.
                The answer will use only information from
                the retrieved pages.
            </p>


            <textarea
                id="question"
                placeholder="What are the main attractions in Luxor?"
            ></textarea>


            <button
                id="ask-button"
                class="ask-button"
                type="button"
            >
                Reveal the Answer
            </button>


            <div class="examples">

                <p>
                    Try an example
                </p>


                <div class="chips">

                    <button
                        class="chip"
                        type="button"
                    >
                        What can tourists see in Alexandria?
                    </button>


                    <button
                        class="chip"
                        type="button"
                    >
                        What is there to do in Aswan?
                    </button>


                    <button
                        class="chip"
                        type="button"
                    >
                        Tell me about the Giza Plateau
                    </button>


                    <button
                        class="chip"
                        type="button"
                    >
                        What are the top attractions in Cairo?
                    </button>

                </div>

            </div>

        </section>


        <!-- =================================================
             RIGHT PANEL
             ================================================= -->

        <section class="panel result-panel">


            <div class="result-title">

                <div>

                    <span class="eyebrow">
                        RAG result
                    </span>

                    <h2>
                        Guide answer
                    </h2>

                </div>


                <span
                    id="result-status"
                    class="status-text"
                >
                    Waiting for a question
                </span>

            </div>


            <div class="result-body">


                <!-- EMPTY STATE -->

                <div
                    id="empty-state"
                    class="empty-state"
                >

                    <div class="empty-icon">
                        🐪
                    </div>

                    <h3>
                        The guide is ready
                    </h3>

                    <p>
                        Ask a question about Egypt to retrieve
                        relevant pages and get a grounded answer.
                    </p>

                </div>


                <!-- ANSWER -->

                <div
                    id="answer-section"
                    class="answer"
                >

                    <p
                        id="answer-question"
                        class="answer-question"
                    ></p>


                    <div
                        id="answer-text"
                        class="answer-box"
                    ></div>


                    <div
                        id="sources-section"
                        class="sources"
                    >

                        <h3>
                            Retrieved sources
                        </h3>

                        <div
                            id="sources-list"
                        ></div>

                    </div>

                </div>

            </div>

        </section>

    </main>


    <!-- =====================================================
         ERROR BAR
         ===================================================== -->

    <div
        id="error-bar"
        class="error-bar"
    ></div>


</div>


<script>

    const apiUrlInput =
        document.getElementById("api-url");

    const healthButton =
        document.getElementById("health-button");

    const healthDot =
        document.getElementById("health-dot");

    const questionInput =
        document.getElementById("question");

    const askButton =
        document.getElementById("ask-button");

    const resultStatus =
        document.getElementById("result-status");

    const emptyState =
        document.getElementById("empty-state");

    const answerSection =
        document.getElementById("answer-section");

    const answerQuestion =
        document.getElementById("answer-question");

    const answerText =
        document.getElementById("answer-text");

    const sourcesSection =
        document.getElementById("sources-section");

    const sourcesList =
        document.getElementById("sources-list");

    const errorBar =
        document.getElementById("error-bar");


    /* ========================================================
       API URL
       ======================================================== */

    function getApiUrl() {

        return apiUrlInput.value
            .trim()
            .replace(/\/$/, "");

    }


    /* ========================================================
       ERROR
       ======================================================== */

    function showError(message) {

        errorBar.textContent = message;

        errorBar.classList.add("show");

    }


    function clearError() {

        errorBar.classList.remove("show");

    }


    /* ========================================================
       TYPE ANSWER
       ======================================================== */

    async function typeAnswer(text) {

        answerText.textContent = "";

        for (const letter of text) {

            answerText.textContent += letter;

            await new Promise(
                resolve => setTimeout(resolve, 8)
            );

        }

    }


    /* ========================================================
       HEALTH CHECK
       ======================================================== */

    healthButton.addEventListener(
        "click",
        async () => {

            clearError();

            healthButton.textContent =
                "Checking...";

            healthButton.disabled =
                true;

            healthDot.className =
                "dot idle";


            try {

                const response =
                    await fetch(
                        `${getApiUrl()}/health`
                    );


                const data =
                    await response.json();


                healthDot.className =
                    data.status === "healthy"
                        ? "dot ok"
                        : "dot error";


                if (data.status !== "healthy") {

                    showError(
                        "The API responded, but its health check was not healthy."
                    );

                }

            }
            catch {

                healthDot.className =
                    "dot error";


                showError(
                    "Could not reach the API. Check the URL and make sure FastAPI is running."
                );

            }


            healthButton.textContent =
                "Ping API";

            healthButton.disabled =
                false;

        }
    );


    /* ========================================================
       ASK QUESTION
       ======================================================== */

    async function askQuestion() {

        clearError();


        const query =
            questionInput.value.trim();


        if (!query) {

            showError(
                "Write a question first."
            );

            return;

        }


        askButton.disabled =
            true;

        askButton.textContent =
            "Searching the guide...";


        resultStatus.textContent =
            "Retrieving pages...";


        emptyState.style.display =
            "none";


        answerSection.style.display =
            "block";


        answerQuestion.textContent =
            `Question: ${query}`;


        answerText.textContent =
            "Consulting the Lonely Planet guide...";


        sourcesList.innerHTML =
            "";


        sourcesSection.style.display =
            "none";


        try {

            const response =
                await fetch(
                    `${getApiUrl()}/query`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            question: query
                        })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Server error (${response.status})`
                );

            }


            const data =
                await response.json();


            await typeAnswer(
                data.answer
            );


            const sources =
                data.sources || [];


            resultStatus.textContent =
                `${sources.length} source${
                    sources.length !== 1
                        ? "s"
                        : ""
                } retrieved`;


            sourcesSection.style.display =
                sources.length
                    ? "block"
                    : "none";


            sources.forEach(
                (source) => {

                    const item =
                        document.createElement(
                            "div"
                        );


                    item.className =
                        "source";


                    const icon =
                        document.createElement(
                            "span"
                        );

                    icon.className =
                        "page-number";

                    icon.textContent =
                        "📜";


                    const text =
                        document.createElement(
                            "span"
                        );

                    text.textContent =
                        source;


                    item.appendChild(
                        icon
                    );

                    item.appendChild(
                        text
                    );


                    sourcesList.appendChild(
                        item
                    );

                }
            );

        }
        catch (error) {

            answerSection.style.display =
                "none";


            emptyState.style.display =
                "grid";


            resultStatus.textContent =
                "Waiting for a question";


            showError(
                error.message ||
                "Could not get an answer from the API."
            );

        }


        askButton.disabled =
            false;


        askButton.textContent =
            "Reveal the Answer";

    }


    askButton.addEventListener(
        "click",
        askQuestion
    );


    /* ========================================================
       CTRL + ENTER
       ======================================================== */

    questionInput.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Enter" &&
                event.ctrlKey
            ) {

                event.preventDefault();

                askQuestion();

            }

        }
    );


    /* ========================================================
       EXAMPLE CHIPS
       ======================================================== */

    document
        .querySelectorAll(".chip")
        .forEach(
            (chip) => {

                chip.addEventListener(
                    "click",
                    () => {

                        questionInput.value =
                            chip.textContent.trim();

                        questionInput.focus();

                    }
                );

            }
        );

</script>

</body>

</html>
"""


# ============================================================
# RENDER
# ============================================================

components.html(
    html,
    height=900,
    scrolling=False,
)