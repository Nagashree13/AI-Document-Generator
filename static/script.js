// =====================================================
// DOCUMENT ELEMENTS
// =====================================================

const documentModeBtn =
    document.getElementById("documentModeBtn");

const databaseModeBtn =
    document.getElementById("databaseModeBtn");

const documentSection =
    document.getElementById("documentSection");

const databaseSection =
    document.getElementById("databaseSection");  


const clearBtn =
    document.getElementById("clearBtn"); 

    


// =====================================================
// DOCUMENT ELEMENTS
// =====================================================

const fileInput =
    document.getElementById("fileInput");

const uploadBox =
    document.getElementById("uploadBox");

const selectedFile =
    document.getElementById("selectedFile");

const fileName =
    document.getElementById("fileName");

const removeFile =
    document.getElementById("removeFile");

const analyzeDocumentBtn =
    document.getElementById(
        "analyzeDocumentBtn"
    );


// =====================================================
// DATABASE ELEMENTS
// =====================================================

const databaseSelect =
    document.getElementById(
        "databaseSelect"
    );

const databaseQuestion =
    document.getElementById(
        "databaseQuestion"
    );

const askDatabaseBtn =
    document.getElementById(
        "askDatabaseBtn"
    );


// =====================================================
// RESULT ELEMENTS
// =====================================================

const loadingSection =
    document.getElementById(
        "loadingSection"
    );

const loadingTitle =
    document.getElementById(
        "loadingTitle"
    );

const loadingMessage =
    document.getElementById(
        "loadingMessage"
    );

const resultSection =
    document.getElementById(
        "resultSection"
    );

const result =
    document.getElementById(
        "result"
    );

const errorBox =
    document.getElementById(
        "errorBox"
    );

const errorMessage =
    document.getElementById(
        "errorMessage"
    );

const copyBtn =
    document.getElementById(
        "copyBtn"
    );

const databaseInfo =
    document.getElementById(
        "databaseInfo"
    );

const resultDatabase =
    document.getElementById(
        "resultDatabase"
    );


// =====================================================
// STATE
// =====================================================

let selectedFileObject = null;


// =====================================================
// INITIALIZATION
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "[UI] Application loaded"
        );

        loadDatabases();

    }
);


// =====================================================
// MODE SWITCH - DOCUMENT
// =====================================================

documentModeBtn.addEventListener(
    "click",
    function () {

        documentModeBtn.classList.add(
            "active"
        );

        databaseModeBtn.classList.remove(
            "active"
        );

        documentSection.style.display =
            "block";

        databaseSection.style.display =
            "none";

        hideError();

        hideResult();

        hideLoading();

    }
);


// =====================================================
// MODE SWITCH - DATABASE
// =====================================================

databaseModeBtn.addEventListener(
    "click",
    function () {

        databaseModeBtn.classList.add(
            "active"
        );

        documentModeBtn.classList.remove(
            "active"
        );

        documentSection.style.display =
            "none";

        databaseSection.style.display =
            "block";

        hideError();

        hideResult();

        hideLoading();

        loadDatabases();

    }
);


// =====================================================
// FILE SELECTION
// =====================================================

fileInput.addEventListener(
    "change",
    function () {

        if (!fileInput.files.length) {

            return;

        }


        const file =
            fileInput.files[0];


        // -------------------------------------------------
        // Check PDF
        // -------------------------------------------------

        if (
            !file.name
                .toLowerCase()
                .endsWith(".pdf")
        ) {

            showError(
                "Please upload a PDF document."
            );

            fileInput.value = "";

            return;

        }


        // -------------------------------------------------
        // Store file
        // -------------------------------------------------

        selectedFileObject = file;


        // -------------------------------------------------
        // Display filename
        // -------------------------------------------------

        fileName.textContent =
            file.name;


        selectedFile.style.display =
            "flex";

        uploadBox.style.display =
            "none";


        hideError();

        hideResult();

        updateDocumentButton();

    }
);


// =====================================================
// REMOVE FILE
// =====================================================

removeFile.addEventListener(
    "click",
    function () {

        selectedFileObject = null;

        fileInput.value = "";

        selectedFile.style.display =
            "none";

        uploadBox.style.display =
            "block";

        updateDocumentButton();

        hideResult();

    }
);


// =====================================================
// UPDATE DOCUMENT BUTTON
// =====================================================

function updateDocumentButton() {

    analyzeDocumentBtn.disabled =
        selectedFileObject === null;

}


// =====================================================
// ANALYZE DOCUMENT
// =====================================================

analyzeDocumentBtn.addEventListener(
    "click",
    async function () {

        if (!selectedFileObject) {

            showError(
                "Please upload a PDF document first."
            );

            return;

        }


        hideError();

        hideResult();


        showLoading(
            "Analyzing document...",
            "Extracting text and generating your summary."
        );


        analyzeDocumentBtn.disabled =
            true;


        try {

            // -------------------------------------------------
            // Create FormData
            // -------------------------------------------------

            const formData =
                new FormData();


            formData.append(
                "file",
                selectedFileObject
            );


            console.log(
                "[UI] Sending document to server..."
            );


            // -------------------------------------------------
            // Send request
            // -------------------------------------------------

            const response =
                await fetch(
                    "/upload",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            console.log(
                "[UI] Document response:",
                data
            );


            // -------------------------------------------------
            // Check response
            // -------------------------------------------------

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Failed to analyze document."
                );

            }


            // -------------------------------------------------
            // Display result
            // -------------------------------------------------

            result.textContent =
                data.summary ||
                data.answer ||
                "No response received.";


            databaseInfo.style.display =
                "none";


            resultSection.style.display =
                "block";


            resultSection.scrollIntoView({
                behavior: "smooth"
            });

        }
        catch (error) {

            console.error(
                "[UI] Document error:",
                error
            );


            showError(
                error.message
            );

        }
        finally {

            hideLoading();

            updateDocumentButton();

        }

    }
);


// =====================================================
// LOAD DATABASES
// =====================================================

async function loadDatabases() {

    try {

        console.log(
            "[UI] Loading databases..."
        );


        // -------------------------------------------------
        // Show loading option
        // -------------------------------------------------

        databaseSelect.innerHTML = `
            <option value="">
                Loading databases...
            </option>
        `;


        databaseSelect.disabled =
            true;


        // -------------------------------------------------
        // Call FastAPI
        // -------------------------------------------------

        const response =
            await fetch(
                "/databases"
            );


        console.log(
            "[UI] Database HTTP status:",
            response.status
        );


        const data =
            await response.json();


        console.log(
            "[UI] Database response:",
            data
        );


        // -------------------------------------------------
        // Check HTTP response
        // -------------------------------------------------

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Could not load databases."
            );

        }


        // -------------------------------------------------
        // Get databases
        // -------------------------------------------------

        let databases =
            data.databases;


        console.log(
            "[UI] Databases received:",
            databases
        );


        // -------------------------------------------------
        // Make sure response is an array
        // -------------------------------------------------

        if (!Array.isArray(databases)) {

            throw new Error(
                "Server did not return a database list."
            );

        }


        // -------------------------------------------------
        // Clear dropdown
        // -------------------------------------------------

        databaseSelect.innerHTML = `
            <option value="">
                Select a database
            </option>
        `;


        // -------------------------------------------------
        // Add each database separately
        // -------------------------------------------------

        databases.forEach(
            function (database) {

                // Convert to string

                database =
                    String(database).trim();


                // Ignore empty values

                if (!database) {

                    return;

                }


                // Ignore database error

                if (
                    database
                        .toLowerCase()
                        .startsWith(
                            "database error:"
                        )
                ) {

                    return;

                }


                // Create option

                const option =
                    document.createElement(
                        "option"
                    );


                option.value =
                    database;


                option.textContent =
                    database;


                databaseSelect.appendChild(
                    option
                );


                console.log(
                    "[UI] Added database:",
                    database
                );

            }
        );


        // -------------------------------------------------
        // Check whether databases were found
        // -------------------------------------------------

        if (
            databaseSelect.options.length === 1
        ) {

            databaseSelect.innerHTML = `
                <option value="">
                    No databases found
                </option>
            `;

            console.warn(
                "[UI] No databases found."
            );

        }


        databaseSelect.disabled =
            false;


        updateDatabaseButton();


        console.log(
            "[UI] Database dropdown updated."
        );

    }
    catch (error) {

        console.error(
            "[UI] Database loading error:",
            error
        );


        databaseSelect.innerHTML = `
            <option value="">
                Failed to load databases
            </option>
        `;


        databaseSelect.disabled =
            false;


        showError(
            "Could not load databases. " +
            error.message
        );

    }

}


// =====================================================
// DATABASE SELECTION
// =====================================================

databaseSelect.addEventListener(
    "change",
    function () {

        console.log(
            "[UI] Selected database:",
            databaseSelect.value
        );


        updateDatabaseButton();

        hideError();

        hideResult();

    }
);


// =====================================================
// DATABASE QUESTION
// =====================================================

databaseQuestion.addEventListener(
    "input",
    function () {

        updateDatabaseButton();

    }
);


// =====================================================
// UPDATE DATABASE BUTTON
// =====================================================

function updateDatabaseButton() {

    const databaseSelected =
        databaseSelect.value
            .trim()
            .length > 0;


    const questionEntered =
        databaseQuestion.value
            .trim()
            .length > 0;


    askDatabaseBtn.disabled =
        !(
            databaseSelected &&
            questionEntered
        );

} 


// =====================================================
// QUESTION EXAMPLES
// =====================================================

document
    .querySelectorAll(
        ".question-example"
    )
    .forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    databaseQuestion.value =
                        button.dataset.question;


                    updateDatabaseButton();

                    hideError();

                    databaseQuestion.focus();

                }
            );

        }
    ); 


// =====================================================
// CLEAR / RESET BUTTON
// =====================================================

document.getElementById("clearBtn").addEventListener("click", function () {
    window.location.href = "/";
});

// =====================================================
// CLEAR / REFRESH BUTTON
// =====================================================

// =====================================================
// CLEAR / REFRESH BUTTON
// =====================================================




// =====================================================
// ASK DATABASE
// =====================================================

askDatabaseBtn.addEventListener(
    "click",
    async function () {

        const database =
            databaseSelect.value.trim();


        const question =
            databaseQuestion.value.trim();


        // -------------------------------------------------
        // Validate database
        // -------------------------------------------------

        if (!database) {

            showError(
                "Please select a database."
            );

            return;

        }


        // -------------------------------------------------
        // Validate question
        // -------------------------------------------------

        if (!question) {

            showError(
                "Please enter a database question."
            );

            return;

        }


        hideError();

        hideResult();


        showLoading(
            "Querying database...",
            "AI is analyzing the database schema and generating SQL."
        );


        askDatabaseBtn.disabled =
            true;


        try {

            console.log(
                "[UI] Sending database question..."
            );


            console.log(
                "[UI] Database:",
                database
            );


            console.log(
                "[UI] Question:",
                question
            );


            // -------------------------------------------------
            // Send request
            // -------------------------------------------------

            const response =
                await fetch(
                    "/database-question",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            question:
                                question,

                            database:
                                database

                        })
                    }
                );


            const data =
                await response.json();


            console.log(
                "[UI] Database answer:",
                data
            );


            // -------------------------------------------------
            // Check response
            // -------------------------------------------------

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Database request failed."
                );

            }


            // -------------------------------------------------
            // Display answer
            // -------------------------------------------------

            result.textContent =
                data.answer ||
                "No answer received.";


            // -------------------------------------------------
            // Display database information
            // -------------------------------------------------

            resultDatabase.textContent =
                data.database ||
                database;


            databaseInfo.style.display =
                "flex";


            // -------------------------------------------------
            // Display result
            // -------------------------------------------------

            resultSection.style.display =
                "block";


            resultSection.scrollIntoView({
                behavior: "smooth"
            });

        }
        catch (error) {

            console.error(
                "[UI] Database error:",
                error
            );


            showError(
                error.message
            );

        }
        finally {

            hideLoading();

            updateDatabaseButton();

        }

    }
);


// =====================================================
// LOADING
// =====================================================

function showLoading(
    title,
    message
) {

    loadingTitle.textContent =
        title;


    loadingMessage.textContent =
        message;


    loadingSection.style.display =
        "block";


    loadingSection.scrollIntoView({
        behavior: "smooth"
    });

}


function hideLoading() {

    loadingSection.style.display =
        "none";

}


// =====================================================
// ERROR
// =====================================================

function showError(
    message
) {

    errorMessage.textContent =
        message;


    errorBox.style.display =
        "flex";

}


function hideError() {

    errorMessage.textContent =
        "";


    errorBox.style.display =
        "none";

}


// =====================================================
// RESULT
// =====================================================

function hideResult() {

    resultSection.style.display =
        "none";


    result.textContent =
        "";


    databaseInfo.style.display =
        "none";

}


// =====================================================
// COPY RESULT
// =====================================================

copyBtn.addEventListener(
    "click",
    async function () {

        try {

            await navigator.clipboard.writeText(
                result.textContent
            );


            copyBtn.textContent =
                "✓ Copied";


            setTimeout(
                function () {

                    copyBtn.textContent =
                        "📋 Copy";

                },
                1500
            );

        }
        catch (error) {

            console.error(
                "[UI] Copy error:",
                error
            );

        }

    }
);