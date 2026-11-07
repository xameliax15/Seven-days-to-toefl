param(
    [string]$OutputDirectory = $PSScriptRoot
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $OutputDirectory)) {
    New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
}

$speech = New-Object -ComObject SAPI.SpVoice
$voiceTokens = $speech.GetVoices()

if ($voiceTokens.Count -lt 2) {
    throw "At least two Windows SAPI voices are required to generate the Day 4 audio."
}

$maleVoice = $voiceTokens.Item(0)
$femaleVoice = $voiceTokens.Item(1)

$questions = @(
    @{
        File = "day4_q1.wav"
        Lines = @(
            @{ Role = "woman"; Text = "Did you reserve the study room for this afternoon?" },
            @{ Role = "man"; Text = "I tried, but every room is booked until five." },
            @{ Role = "woman"; Text = "Then let's meet at the tables near the second-floor windows. They're usually quiet." },
            @{ Role = "man"; Text = "Good idea. I'll tell the rest of the group." }
        )
        Question = "What are the speakers mainly discussing?"
    },
    @{
        File = "day4_q2.wav"
        Lines = @(
            @{ Role = "man"; Text = "I can't find my flash drive. I thought I left it beside the computer." },
            @{ Role = "woman"; Text = "You put it in the small pocket of your blue folder after the presentation. I saw you zip it closed." },
            @{ Role = "man"; Text = "You're right. It's still there." }
        )
        Question = "Where is the man's flash drive?"
    },
    @{
        File = "day4_q3.wav"
        Lines = @(
            @{ Role = "woman"; Text = "Are you coming to the review session tonight?" },
            @{ Role = "man"; Text = "I have a statistics report due first thing tomorrow morning." },
            @{ Role = "woman"; Text = "So I should tell the tutor you can't make it?" },
            @{ Role = "man"; Text = "Unfortunately, yes." }
        )
        Question = "Why does the man mention his statistics report?"
    },
    @{
        File = "day4_q4.wav"
        Lines = @(
            @{ Role = "man"; Text = "The printer in the library is out of paper, and I need to submit this form before four." },
            @{ Role = "woman"; Text = "Why don't you use the printer in the student center? It's working, and the line was short when I passed it." },
            @{ Role = "man"; Text = "I'll go there now. Thanks." }
        )
        Question = "What does the woman suggest the man do?"
    },
    @{
        File = "day4_q5.wav"
        Lines = @(
            @{ Role = "woman"; Text = "You look relieved. Did the professor return your essay?" },
            @{ Role = "man"; Text = "Yes. I expected a lot of corrections, but she only marked two sentences." },
            @{ Role = "woman"; Text = "All that revising paid off, then." }
        )
        Question = "What can be inferred about the man's essay?"
    }
)

function Set-SpeakerVoice {
    param([string]$Role)

    if ($Role -eq "woman") {
        $speech.Voice = $femaleVoice
        $speech.Rate = 0
    }
    elseif ($Role -eq "man") {
        $speech.Voice = $maleVoice
        $speech.Rate = 0
    }
    else {
        $speech.Voice = $maleVoice
        $speech.Rate = -1
    }
}

function Add-SpeechPause {
    param([int]$Milliseconds)

    [void]$speech.Speak("<silence msec=`"$Milliseconds`" />", 8)
}

$questionNumber = 0

foreach ($question in $questions) {
    $questionNumber += 1
    $outputPath = Join-Path $OutputDirectory $question.File
    $stream = New-Object -ComObject SAPI.SpFileStream

    try {
        $stream.Open($outputPath, 3, $false)
        $speech.AudioOutputStream = $stream

        Set-SpeakerVoice "narrator"
        [void]$speech.Speak("Question $questionNumber.")
        Add-SpeechPause 500

        foreach ($line in $question.Lines) {
            Set-SpeakerVoice $line.Role
            [void]$speech.Speak($line.Text)
            Add-SpeechPause 420
        }

        Add-SpeechPause 350
        Set-SpeakerVoice "narrator"
        [void]$speech.Speak($question.Question)
    }
    finally {
        $stream.Close()
        $speech.AudioOutputStream = $null
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($stream)
    }
}

[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($femaleVoice)
[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($maleVoice)
[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($voiceTokens)
[void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($speech)

Get-ChildItem -LiteralPath $OutputDirectory -Filter "day4_q*.wav" |
    Sort-Object Name |
    Select-Object Name, Length, LastWriteTime
