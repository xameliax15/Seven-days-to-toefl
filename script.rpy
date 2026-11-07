# Prolog Seven Days to TOEFL

default player_name = "Pemain"
default player_gender = "female"
default story_run_id = ""
default persistent.ending_gallery = {}
default persistent.completed_story_runs = {}
default day = 0
default target_score = 400
default study_calendar_unlocked = False
default calendar_completed_day = 0
default calendar_resume_label = ""
default calendar_continue_label = ""
default day_1_choice = ""
default day_1_status = "not_started"
default day_1_vocab_score = 0
default day_1_makeup_pending = False
default day_1_summary_seen = False
default day_1_group_reply = ""
default day_1_packed_items = []
default extra_practice_score = 0
default extra_practice_days = []
default day_2_choice = ""
default day_2_status = "not_started"
default day_2_makeup_pending = False
default day_2_structure_score = 0
default day_2_summary_seen = False
default day_2_group_reply = ""
default day_3_choice = ""
default day_3_status = "not_started"
default day_3_makeup_pending = False
default day_3_reading_score = 0
default day_3_summary_seen = False
default day_3_group_reply = ""
default day_4_choice = ""
default day_4_status = "not_started"
default day_4_makeup_pending = False
default day_4_listening_score = 0
default day_4_summary_seen = False
default day_4_group_reply = ""
default day_4_backlog_plan_made = False
default day_5_choice = ""
default day_5_status = "not_started"
default day_5_makeup_pending = False
default day_5_structure_score = 0
default day_5_summary_seen = False
default day_5_group_reply = ""
default day_5_backlog_checkin = False
default day_5_cleared_makeup = ""
default day_6_status = "not_started"
default day_6_makeup_pending = False
default day_6_review_score = 0
default day_6_review_streak = 0
default day_6_travel_choice = ""
default day_6_drink_choice = ""
default day_6_backlog_checkin = False
default day_6_cleared_makeup = ""
default day_6_final_reply = ""
default day_7_status = "not_started"
default day_7_packed_items = []
default day_7_class_items = []
default day_7_used_items = []
default day_7_face_scanned = False
default day_7_room_scanned = False
default day_7_scanned_points = []
default day_7_exam_score = 0
default day_7_exam_question = 0
default day_7_final_score = 0
default day_7_ending = ""
default day_7_cheating_detected = False
default day_7_cheating_items = []

init python:
    def story_day_label(day_number):
        return {
            1: "day_1_morning",
            2: "day_2_morning",
            3: "day_3_afternoon",
            4: "day_4_afternoon",
            5: "day_5_afternoon",
            6: "day_6_afternoon",
            7: "day_7_morning",
        }.get(day_number)

    def selected_study_day(value):
        """Nilai tombol BATAL (cancel/True/None) tidak boleh dibanding dengan nomor hari."""
        return value if isinstance(value, int) else None

    def toggle_inventory_item(items, item_name):
        """Mengembalikan daftar barang terpilih tanpa memodifikasi list screen secara langsung."""
        selected = list(items)
        if item_name in selected:
            selected.remove(item_name)
        else:
            selected.append(item_name)
        return selected

    def study_hint_level(previous_score):
        """Mengubah akumulasi skor hari sebelumnya menjadi level hint."""
        # Hint Hari 7 baru tersedia setelah pemain mengumpulkan poin hari sebelumnya.
        if previous_score >= 200:
            return 3
        elif previous_score >= 100:
            return 2
        elif previous_score >= 30:
            return 1
        return 0

    def study_hint_for(category):
        hints = {
            "vocabulary": "Terjemahkan hubungan kalimatnya terlebih dahulu. Cari definisi, kontras, contoh, atau sebab-akibat di sekitar kata target.",
            "structure": "Terjemahkan kerangka kalimat, lalu tandai subject, finite verb, clause, dan pola yang sejajar. Periksa agreement sebelum memilih bentuk.",
            "reading": "Terjemahkan ide umum passage. Bedakan main idea, detail pendukung, reference, dan inference; hindari pilihan yang terlalu mutlak.",
            "listening": "Catat keyword, perubahan informasi, intent, dan respons terakhir. Satu kata yang terlewat tidak otomatis mengubah makna dialog.",
            "mixed": "Terjemahkan konteks, identifikasi skill yang diuji, lalu cari bukti sebelum membandingkan pilihan. Hint ini tidak menampilkan jawaban."
        }
        return hints.get(category, hints["mixed"])

    def day7_phone_dragged(drags, drop):
        """Mencatat titik ruangan ketika smartphone dijatuhkan pada target scan."""
        if drop is None:
            return None
        drag_name = getattr(drop, "drag_name", "")
        if drag_name.startswith("scan_"):
            point = drag_name[5:]
            if point not in store.day_7_scanned_points:
                store.day_7_scanned_points.append(point)
                renpy.restart_interaction()
        return None

    def day7_detect_cheating(items):
        """Mencatat buku/catatan dan perangkat audio yang terlihat kamera."""
        prohibited = {"notebook": "buku catatan", "earphone": "earphone/perangkat audio"}
        return [prohibited[item] for item in (items or []) if item in prohibited]

    def day7_ending_title(exam_score, total_score, cheating=False):
        if cheating and exam_score >= 500:
            return "ENDING X - NILAI TINGGI, TERDETEKSI CURANG"
        elif cheating and total_score >= target_score:
            return "ENDING Y - LULUS SKOR, TERDETEKSI CURANG"
        elif cheating:
            return "ENDING Z - TIDAK LULUS DAN TERDETEKSI CURANG"
        if exam_score >= 500:
            return "ENDING S - NILAI TINGGI"
        elif total_score >= target_score:
            return "ENDING A - LULUS DI ATAS 400"
        return "ENDING C - TIDAK LULUS (DI BAWAH 400)"

    def day7_audio_for_question(question_index):
        """Audio Listening sesi 3 memakai bank WAV yang sudah ada."""
        if question_index >= 40:
            audio_number = ((question_index - 40) // 4) + 1
            return "audio/day4/day4_q%d.wav" % audio_number
        return None

    def day7_question_time(section_label):
        """Batas waktu per soal, dibuat berbeda sesuai sesi ujian."""
        if "LISTENING" in section_label:
            return 60
        elif "READING" in section_label:
            return 90
        return 45

init -20 python:
    renpy.music.register_channel(
        "listening",
        mixer="voice",
        loop=False,
        stop_on_mute=True,
        tight=False,
        buffer_queue=True
    )

define audio.day4_q1 = "audio/day4/day4_q1.wav"
define audio.day4_q2 = "audio/day4/day4_q2.wav"
define audio.day4_q3 = "audio/day4/day4_q3.wav"
define audio.day4_q4 = "audio/day4/day4_q4.wav"
define audio.day4_q5 = "audio/day4/day4_q5.wav"
define audio.bgm_main_menu = "audio/bgm/main_menu_night.mp3"
define audio.bgm_campus = "audio/bgm/campus_theme.mp3"
define audio.bgm_study = "audio/bgm/study_lofi.mp3"
define audio.bgm_comedy = "audio/bgm/comedy_panic.mp3"
define audio.bgm_quiz = "audio/bgm/quiz_thinking.mp3"
define audio.bgm_cafe = "audio/bgm/cafe_review.mp3"
define audio.bgm_exam = "audio/bgm/exam_tension.mp3"
define audio.bgm_master = "audio/bgm/ending_master.mp3"
define audio.bgm_hopeful = "audio/bgm/ending_hopeful.mp3"
define audio.bgm_violation = "audio/bgm/ending_violation.mp3"
define audio.sfx_notification = "audio/ui/ui_notification.mp3"

define player = DynamicCharacter("player_name", color="#67e8f9")
define reza = Character("Reza", color="#fbbf24")
define bima = Character("Bima", color="#60a5fa")
define maya = Character("Maya", color="#f472b6")
define rina = Character("Rina", color="#34d399")
define leo = Character("Leo", color="#c4b5fd")
define teacher = Character("Ibu Diah", color="#f0abfc")
define system = Character("Sistem", color="#22d3ee", what_italic=True)
define day_one_speaker_swap = Dissolve(0.15)
define day_three_reading_passage = "Many cities plant trees along streets to improve urban environments. Trees provide shade, which lowers surface temperatures on roads and sidewalks during hot weather. Their leaves also trap some airborne particles, although trees cannot replace efforts to reduce pollution at its source. In addition, green spaces may encourage residents to walk and spend time outdoors. However, urban trees need careful planning. A species that grows well in one region may struggle in another because of differences in rainfall, soil, or temperature. Young trees also require regular watering and protection from damage. For these reasons, successful tree-planting programs do more than put trees in the ground; they select suitable species and provide long-term care. This planning allows communities to receive the benefits of trees for many years."
define day_six_reading_passage = "Short breaks can improve study sessions when they are planned. A few minutes away from a difficult task may reduce mental fatigue and help learners return with better attention. However, breaks are less useful when they have no limit or become a way to avoid the task. Effective learners decide when the break will end and what they will do next."
init python:
    def build_day7_exam_questions():
        def q(section, prompt, a, b, c, correct, hint):
            return (section, prompt, a, b, c, correct, hint)

        questions = []
        vocab = [
            ("Concise instructions helped everyone finish quickly. What does concise mean?", "Very brief", "Very expensive", "Impossible to follow", "a", "Cari sinonim yang berhubungan dengan instruksi singkat dan jelas."),
            ("The evidence was compelling, so the committee accepted the proposal. What does compelling mean?", "Persuasive", "Unrelated", "Temporary", "a", "Lihat akibatnya: committee menerima proposal karena bukti itu meyakinkan."),
            ("The researcher observed a gradual decline in errors. What does gradual mean?", "Happening slowly", "Happening suddenly", "Happening secretly", "a", "Konteks decline menunjukkan perubahan yang tidak terjadi sekaligus."),
            ("The word ambiguous describes a sentence that is...", "Open to more than one interpretation", "Easy to memorize", "Written in the past tense", "a", "Cari hubungan ambiguous dengan kebutuhan meminta klarifikasi."),
            ("The student retained the information after reviewing it. What does retained mean?", "Kept or remembered", "Forgot completely", "Translated incorrectly", "a", "Reviewing memberi petunjuk bahwa informasi tetap tersimpan dalam ingatan."),
            ("A reliable source is one that is...", "Trustworthy", "Unfinished", "Unusual", "a", "Hubungkan source dengan kepercayaan terhadap informasi."),
            ("The new schedule is feasible for the study group. What does feasible mean?", "Practical and possible", "Dangerous", "Already cancelled", "a", "Jadwal yang bisa dijalankan adalah practical and possible."),
            ("The tutor clarified the rule. What did the tutor do?", "Made it easier to understand", "Made it longer", "Removed every example", "a", "Clarify berkaitan dengan membuat sesuatu menjadi jelas."),
            ("The results were consistent across three tests. What does consistent mean?", "Similar and stable", "Random every time", "Hidden from readers", "a", "Tiga tes menghasilkan pola yang sama, bukan acak."),
            ("The instruction was mandatory. What does mandatory mean?", "Required", "Optional", "Postponed", "a", "Mandatory berlawanan dengan optional."),
        ]
        for prompt, a, b, c, correct, hint in vocab:
            questions.append(q("SESI 1 • VOCABULARY", prompt, a, b, c, correct, hint))

        grammar = [
            ("The list of required items ___ on the desk.", "is", "are", "be", "a", "Subject utama list tunggal; of required items hanya modifier."),
            ("The students ___ their notes before the teacher arrived.", "review", "reviewed", "reviewing", "b", "Before dan arrived menempatkan kegiatan pada masa lampau."),
            ("Neither the headphones nor the phone ___ missing.", "is", "are", "be", "a", "Pada neither...nor, verb mengikuti subject terdekat: phone tunggal."),
            ("The proctor asked us ___ the camera on.", "keep", "to keep", "keeping", "b", "Pola ask someone to do something membutuhkan infinitive."),
            ("Only after the scan ___ the test begin.", "can", "did", "does", "b", "Inversi setelah Only after untuk kejadian lampau memakai did."),
            ("The report, together with the answer sheets, ___ ready.", "is", "are", "were", "a", "Together with tidak mengubah subject utama report."),
            ("The candidates ___ waiting when the announcement started.", "were", "was", "be", "a", "Candidates plural dan aksi sedang berlangsung di masa lampau."),
            ("The teacher recommended that every student ___ calm.", "remain", "remains", "remaining", "a", "Setelah recommend that, gunakan base verb dalam subjunctive."),
            ("The phone must ___ on the table during the exam.", "remain", "remains", "remaining", "a", "Setelah modal must gunakan base verb."),
            ("The answers were checked carefully before they ___ submitted.", "were", "was", "be", "a", "They plural, sehingga passive past memakai were."),
        ]
        for prompt, a, b, c, correct, hint in grammar:
            questions.append(q("SESI 1 • GRAMMAR", prompt, a, b, c, correct, hint))

        reading_sets = [
            ("PASSAGE A • STUDY ROUTINES", "A short routine before studying can reduce hesitation. Learners who prepare their materials, set a time limit, and choose one clear goal often begin faster. The routine does not guarantee perfect concentration, but it removes small decisions that can delay the first task.", [
                ("What is the main idea?", "A simple preparation routine can help learners start efficiently.", "Long routines always guarantee concentration.", "Learners should avoid setting goals.", "a", "Main idea mencakup routine, persiapan, dan dampaknya pada awal belajar."),
                ("What does the routine remove?", "Small decisions that delay starting", "All difficult questions", "The need for a time limit", "a", "Cari kalimat terakhir tentang small decisions yang delay the first task."),
                ("The word hesitation is closest in meaning to...", "Uncertainty before acting", "A final answer", "A long celebration", "a", "Hesitation terjadi sebelum seseorang mulai bertindak."),
                ("What can be inferred about the routine?", "It supports starting but does not make concentration perfect.", "It replaces every study strategy.", "It works only for group discussions.", "a", "Penulis secara eksplisit membatasi klaim: tidak menjamin konsentrasi sempurna."),
                ("Why does the author mention one clear goal?", "To reduce the number of decisions before starting", "To make the session endless", "To avoid preparing materials", "a", "Satu goal adalah bagian dari keputusan kecil yang disederhanakan."),
            ]),
            ("PASSAGE B • CAMPUS TREES", "The university planted trees beside the language laboratory. Their shade makes the walkway cooler, and their roots help reduce soil erosion after heavy rain. The project also created a quieter outdoor area, although the trees will need regular care while they are young.", [
                ("What is the passage mainly about?", "Benefits and maintenance needs of a campus tree project", "Reasons to remove all campus trees", "A laboratory experiment about roots", "a", "Jawaban harus mencakup manfaat dan kebutuhan perawatan."),
                ("What makes the walkway cooler?", "The shade from the trees", "The laboratory windows", "Heavy rain", "a", "Detail langsung ada pada kalimat kedua."),
                ("The word erosion refers to...", "Soil being worn away", "A new language course", "A type of laboratory light", "a", "Roots membantu mengurangi soil erosion setelah hujan."),
                ("What does although signal?", "A contrast between the quiet area and the need for care", "A chronological list", "A definition of shade", "a", "Although memperkenalkan informasi yang berlawanan atau membatasi."),
                ("What will the trees need?", "Regular care while young", "A new laboratory", "More heavy rain", "a", "Informasi eksplisit berada di akhir passage."),
            ]),
            ("PASSAGE C • DIGITAL FEEDBACK", "Digital practice tools can show an answer immediately, but instant feedback is not automatically useful. Learners improve more when they read the explanation, identify the rule, and try a similar item. Checking only the score may create the illusion of progress without changing the underlying mistake.", [
                ("What is the main point?", "Feedback helps most when learners analyze and apply it.", "Scores should never be recorded.", "Digital tools cannot show explanations.", "a", "Main idea menekankan cara menggunakan feedback, bukan sekadar melihat skor."),
                ("What should learners identify?", "The rule behind the mistake", "The color of the screen", "The length of the passage", "a", "Kalimat kedua menyebut identify the rule."),
                ("The word illusion is closest to...", "A misleading impression", "A confirmed result", "A study schedule", "a", "Checking score saja bisa menciptakan kesan kemajuan yang menipu."),
                ("What may happen if learners check only scores?", "Their underlying mistake may remain.", "They will master every rule.", "They will stop receiving feedback.", "a", "Penulis menghubungkan score-only dengan mistake yang tidak berubah."),
                ("Which action best follows the passage?", "Read an explanation and attempt a similar question", "Skip every explanation", "Record only the highest score", "a", "Ini menggabungkan dua strategi yang dianjurkan penulis."),
            ]),
            ("PASSAGE D • TEST ANXIETY", "Test anxiety often grows when an unfamiliar task is treated as a single enormous threat. Breaking the task into sections can make the next action visible. Breathing slowly may lower tension, but preparation with the real format remains necessary. A calm body and a practiced strategy work together.", [
                ("What is the main idea?", "Managing anxiety works best with calmness and format-specific preparation.", "Breathing alone guarantees success.", "Large tasks should never be divided.", "a", "Pilih ringkasan yang mencakup calm body dan practiced strategy."),
                ("What can make the next action visible?", "Breaking the task into sections", "Ignoring the format", "Increasing the threat", "a", "Detail langsung dari kalimat kedua."),
                ("The word unfamiliar means...", "Not known through experience", "Already mastered", "Located outdoors", "a", "Unfamiliar adalah sesuatu yang belum dikenal."),
                ("What does but signal in the third sentence?", "Breathing helps, yet preparation is still needed", "The exam has ended", "Preparation is unnecessary", "a", "But menunjukkan pembatasan terhadap manfaat breathing."),
                ("What works together according to the passage?", "A calm body and a practiced strategy", "A large threat and confusion", "A score and an empty schedule", "a", "Jawaban terdapat pada kalimat terakhir."),
            ]),
        ]
        for title, passage, items in reading_sets:
            for prompt, a, b, c, correct, hint in items:
                questions.append(q("SESI 2 • READING", title + "\n\n" + passage + "\n\n" + prompt, a, b, c, correct, hint))

        listening = [
            ("Audio: Woman: Did you reserve the study room? Man: Every room is booked until five. Woman: Let's meet at the tables near the second-floor windows. What are they mainly discussing?", "A place to meet", "A cancelled exam", "A missing flash drive", "a", "Tangkap perubahan dari study room yang penuh menuju tables near windows."),
            ("Audio: The tables near the second-floor windows are usually quiet. Why are they chosen?", "They are usually quiet", "They have new computers", "They are beside the printer", "a", "Alasan pilihan disebut langsung setelah lokasi."),
            ("Audio: The man says, 'Good idea. I'll tell the rest of the group.' What will he do?", "Tell the group about the meeting place", "Reserve every study room", "Call the proctor", "a", "Respons terakhir menunjukkan tindakan berikutnya."),
            ("Audio: Which statement is true about the study room?", "It is booked until five", "It is empty all afternoon", "It is on the first floor", "a", "Detail waktu muncul pada respons man."),
            ("Audio: Man: I cannot find my flash drive. Woman: You put it in the small pocket of your blue folder. Where is it?", "In the small pocket of a blue folder", "Beside the computer", "Inside the study room", "a", "The woman corrects the man's first assumption."),
            ("Audio: What did the man initially think?", "He left the flash drive beside the computer", "He submitted the presentation", "He lost his blue folder", "a", "I thought I left it beside the computer adalah dugaan awal."),
            ("Audio: How does the woman know where the flash drive is?", "She saw him zip the folder", "She printed a new one", "She asked the tutor", "a", "Bukti berasal dari kalimat I saw you zip it closed."),
            ("Audio: What is the man's reaction at the end?", "He realizes it is still in the folder", "He cancels the presentation", "He leaves the campus", "a", "You're right confirms the correction."),
            ("Audio: Woman: Are you coming to the review session? Man: I have a statistics report due tomorrow. Why will he miss it?", "He has a report due soon", "He is travelling", "The tutor cancelled it", "a", "Statistics report due first thing tomorrow is the reason."),
            ("Audio: What does the woman offer to do?", "Tell the tutor he cannot attend", "Write the statistics report", "Move the session to noon", "a", "So I should tell the tutor shows the offer."),
            ("Audio: When is the statistics report due?", "First thing tomorrow morning", "Next month", "After the review session", "a", "Waktu disebut eksplisit oleh man."),
            ("Audio: What can be inferred about the man?", "He has another urgent academic responsibility", "He dislikes all review sessions", "He has no assignment", "a", "Inference menggabungkan due date dan ketidakhadiran."),
            ("Audio: Man: The library printer is out of paper. Woman: Use the printer in the student center. What does she suggest?", "Use the student center printer", "Buy paper for the library", "Submit the form tomorrow", "a", "Why don't you use menandai suggestion."),
            ("Audio: Why does the man need a printer?", "He must submit a form before four", "He wants to print a novel", "He is preparing a lecture", "a", "Kebutuhan waktu disebut pada kalimat pertama."),
            ("Audio: What evidence supports the woman's suggestion?", "The student-center printer is working and the line was short", "The library is closed", "The form is missing", "a", "Working dan short line menjadi alasan praktis."),
            ("Audio: What will the man probably do next?", "Go to the student center", "Wait until next week", "Buy a new computer", "a", "I'll go there now mengonfirmasi tindakan."),
            ("Audio: Woman: Did the professor return your essay? Man: She only marked two sentences. What can be inferred?", "The essay needed only a few corrections", "The essay was never submitted", "The professor rejected it", "a", "Only two sentences dan revising paid off menunjukkan hasil baik."),
            ("Audio: How does the man feel?", "Relieved", "Confused about the room", "Angry at the printer", "a", "Woman says You look relieved."),
            ("Audio: What did the professor do?", "Marked two sentences", "Rewrote the entire essay", "Lost the essay", "a", "Detail langsung dari respons man."),
            ("Audio: What is the meaning of 'paid off' in this context?", "The revision effort produced a good result", "The essay required payment", "The class was postponed", "a", "Paid off berarti usaha memberikan hasil."),
        ]
        for prompt, a, b, c, correct, hint in listening:
            questions.append(q("SESI 3 • LISTENING", prompt, a, b, c, correct, hint))
        return tuple(questions)

define day_7_exam_questions = build_day7_exam_questions()

# Aset yang tersedia dipakai sebagai sprite sementara. Nama alias ini membuat
# aset mudah diganti nanti tanpa perlu mengubah dialog.
image bg cafeteria = Transform("images/kantin.png", xysize=(1920, 1080))
image bg player bedroom = Transform("images/bg_player_bedroom_evening.png", xysize=(1920, 1080))
image bg player bedroom morning = Transform("images/bg_player_bedroom_morning.png", xysize=(1920, 1080))
image bg player bedroom afternoon = Transform("images/bg_player_bedroom_morning.png", xysize=(1920, 1080))
image bg campus morning = Transform("images/download.jpg", xysize=(1920, 1080))
image bg library study = Transform("images/bg_library_study_morning.png", xysize=(1920, 1080))
image bg language laboratory = Transform("images/bg_library_study_morning.png", xysize=(1920, 1080))
image bg day6 journey afternoon = Transform("images/bg_day6_journey_afternoon.png", xysize=(1920, 1080))
image bg day6 journey evening = Transform("images/bg_day6_journey_afternoon.png", xysize=(1920, 1080), matrixcolor=BrightnessMatrix(-0.14))
image bg day6 cafe afternoon = Transform("images/bg_day6_cafe_afternoon.png", xysize=(1920, 1080))
image bg day6 cafe sunset = Transform("images/bg_day6_cafe_sunset.png", xysize=(1920, 1080))
image bg day6 cafe evening = Transform("images/bg_day6_cafe_sunset.png", xysize=(1920, 1080), matrixcolor=BrightnessMatrix(-0.10))
image bg day7 study desk = Transform("images/bg_day7_study_desk.png", xysize=(1920, 1080))
image bg day7 exam classroom = Transform("images/bg_day7_exam_classroom.png", xysize=(1920, 1080))
image bg day7 exam desk = Transform("images/bg_day7_exam_desk.png", xysize=(1920, 1080))
image bg main menu night = Transform("images/bg_main_menu_night.png", xysize=(1920, 1080))
# Variasi latar menu dengan Player yang sesuai gender pilihan pemain.
# Maya, Leo, dan Rina sudah menyatu di dalam ilustrasi latar.
image bg main menu night male = Transform("images/bg_main_menu_player_male.png", xysize=(1920, 1080))
image bg main menu night female = Transform("images/bg_main_menu_player_female.png", xysize=(1920, 1080))
image bg black = Solid("#050812")
image weather rain overlay = Solid("#263b526b")
image day7 item notebook = "images/day7_items/notebook.png"
image day7 item pencil = "images/day7_items/pencil.png"
image day7 item eraser = "images/day7_items/eraser.png"
image day7 item phone = "images/day7_items/phone.png"
image day7 item id_card = "images/day7_items/id_card.png"
image day7 item water = "images/day7_items/water.png"
image day7 item earphone = "images/day7_items/earphone.png"
image maya neutral = "images/maya.png"
image leo neutral = "images/leo.png"
image rina neutral = "images/rina.png"
image reza neutral = "images/reza.png"
image bima neutral = "images/bima.png"
image mc female neutral = "images/f_player.png"
image mc male neutral = "images/m_player.png"
image mc neutral = ConditionSwitch(
    "player_gender == 'male'", "images/m_player.png",
    "True", "images/f_player.png"
)
image normal_speaker maya = "images/maya.png"
image normal_speaker leo = "images/leo.png"
image normal_speaker rina = "images/rina.png"
image normal_speaker reza = "images/reza.png"
image normal_speaker bima = "images/bima.png"
image normal_speaker player = ConditionSwitch(
    "player_gender == 'male'", "images/m_player.png",
    "True", "images/f_player.png"
)

transform vn_left:
    xalign 0.12
    yalign 1.0
    zoom 0.62

transform vn_center:
    xalign 0.5
    yalign 1.0
    zoom 0.62

transform vn_right:
    xalign 0.88
    yalign 1.0
    zoom 0.62

transform screen_shake:
    xoffset 0
    linear 0.04 xoffset -18
    linear 0.04 xoffset 18
    linear 0.04 xoffset -12
    linear 0.04 xoffset 12
    linear 0.04 xoffset 0


label start:
    scene bg black
    play music audio.bgm_campus loop fadein 1.0
    $ story_run_id = "run-%d" % renpy.random.randint(100000000, 999999999)
    $ player_name = renpy.call_screen("player_name_input")
    if not player_name.strip():
        $ player_name = "Pemain"

    $ player_gender = renpy.call_screen("player_gender_selection")

    jump prologue_cafeteria


label prologue_cafeteria:
    scene bg cafeteria with fade
    play music audio.bgm_comedy loop fadein 0.5
    show mc neutral at vn_center with dissolve
    system "Kantin FTI UNIBBA — sore hari. Suara mahasiswa, denting sendok, dan ketikan keyboard menyatu dengan musik lo-fi yang santai."

    show reza neutral at vn_left with dissolve
    reza "Haaah... Akhirnya kelar juga debugging kode programku. Otakku rasanya udah kayak RAM yang sisa kapasitasnya tinggal dua persen. Mau meledak!"

    show bima neutral at vn_right with dissolve
    bima "Reza, jangan berisik! Ini aku lagi war penting! Awas, healer-ku mati, woi! Cover aku dari kiri!"

    hide reza with dissolve
    show maya neutral at vn_left with dissolve
    maya "Kalian ini kebiasaan banget. Baru selesai kelas Basis Data bukannya pendinginan otak malah sibuk sendiri-sendiri. Eh, Rina ke mana? Lama banget beli siomaynya."
    player "Rina lagi antre, tadi sih katanya—"

    # Record scratch, notifikasi, dan BGM bisa ditambahkan ke kanal audio ketika
    # berkas audionya sudah tersedia.
    hide mc with dissolve
    with vpunch
    system "TING! TING! TING! TING!"
    show rina neutral at vn_center with moveinright
    rina "Teman-teman!! Kalian udah buka grup WA angkatan belum?! Baca sekarang! Darurat akademik!"
    bima "Yah, karakterku mati kan kaget denger suara WA beruntun! Ada apa sih heboh banget?!"
    show reza neutral at vn_left
    hide maya
    reza "Paling info dosen pengganti untuk besok pagi..."

    play sound audio.sfx_notification
    call screen whatsapp_announcement

    reza "HAH?! MINGGU DEPAN?! Kampus ini hobi banget ngasih jumpscare akademik! Aku belum nyentuh materi grammar sama sekali semenjak semester satu!"
    rina "Gawat! Waktunya cuma tujuh hari! Nilai Listening-ku hancur. Kalau native speaker-nya ngomong terlalu cepat, aku langsung nge-blank!"

    hide reza
    show maya neutral at vn_left with dissolve
    maya "Aduh, kalian drama banget. Standarnya kan target skor 400 di rentang TOEFL ITP 310–677, itu masih level dasar. Tinggal hitung kancing A, B, C, D juga tembus kalau amal kalian lagi bagus."
    bima "Nggak bisa pakai sistem gacha, Maya! Ini Sudden Boss Event yang taruhannya masa depan! Kalau skor kita nggak nyentuh 400, kita kena Game Over berjamaah!"
   
    hide maya with dissolve
    show mc neutral at vn_left with dissolve
    player "Bima benar. Kita nggak bisa cuma mengandalkan keberuntungan. Gimana kalau mulai besok kita bikin Study Group intensif selama seminggu penuh?"
    rina "Ide bagus, [player_name]! Tapi siapa yang mampu ngajarin kita? Kita berempat sama-sama jadi beban kalau urusan bahasa Inggris."

    hide mc
    hide bima
    hide rina
    with dissolve
    system "Hening sejenak. Pandangan mereka serempak beralih ke ujung meja."

    # Leo muncul sendirian di tengah
    show leo neutral at vn_center with dissolve
    system "Di sana Leo duduk dengan headphone hitam, membaca novel tebal berbahasa Inggris seolah keributan tadi tidak pernah terjadi."

    # Bima muncul di kiri, Leo geser ke kanan agar tidak tabrakan
    show leo neutral at vn_right with dissolve
    show bima neutral at vn_left with dissolve
    bima "Cuma ada satu High-Level Player di party kita yang bisa nge-carry raid ini..."

    # Maya masuk di tengah (Bima kiri, Leo kanan)
    show maya neutral at vn_center with dissolve
    maya "Biar aku yang urus."

    # Leo bicara — Bima kiri, Maya tengah, Leo kanan
    leo "Apa? Kalau kalian mau pinjam charger, colokannya ada di bawah meja."

    # Maya bicara — sudah di tengah
    maya "Bukan charger, Leo yang baik hati dan super pintar. Boleh nggak kamu bimbing Study Group kita selama seminggu? Nilai TOEFL-mu sudah 550."

    # Reza bicara — ganti Bima di kiri dengan Reza
    hide bima with dissolve
    show reza neutral at vn_left with dissolve
    reza "Tolonglah, Tuan Muda Leo! Selamatkan hamba dari ancaman DO terselubung ini!"

    # Bima bicara — ganti Reza di kiri dengan Bima
    hide reza with dissolve
    show bima neutral at vn_left with dissolve
    bima "Anggap aja ini misi escort level Hard, Leo!"

    # Leo bicara — Bima kiri, Maya tengah, Leo kanan
    leo "Seminggu penuh? Aku biasanya belajar sendiri. Mengajari satu kelompok akan membutuhkan banyak waktu dan keseriusan dari kalian."

    # Rina bicara — ganti Bima di kiri dengan Rina
    hide bima with dissolve
    show rina neutral at vn_left with dissolve
    rina "Leo... masa kamu tega melihat teman-temanmu tertinggal skripsi? Kita traktir makan siang sebulan!"

    # Leo bicara — Rina kiri, Maya tengah, Leo kanan
    leo "Aku nggak butuh traktiran. Baiklah, aku akan membantu. Tapi selama tujuh hari ini kalian harus datang tepat waktu, mengerjakan latihan, dan benar-benar mendengarkan materi yang kujelaskan."

    # Maya bicara — sudah di tengah
    maya "Nah, begitu dong! Materinya bakal mulai dari mana?"

    # Leo bicara — sudah di kanan
    leo "Kita mulai dari Vocabulary dasar, lanjut ke Structure dan Grammar, lalu berlatih Reading dan Listening. Setiap hari aku akan menjelaskan konsep, memberi contoh soal, kemudian membahas kesalahan kalian satu per satu."

    # Rina bicara — sudah di kiri
    rina "Berarti kita punya jadwal belajar dan materi yang jelas untuk tujuh hari?"

    # Leo bicara — sudah di kanan
    leo "Iya. Hari terakhir kita lakukan simulasi dan evaluasi. Kalau kalian disiplin, target skor 400 masih sangat mungkin dicapai."

    # Pergantian scene: hanya MC dan Leo
    hide rina with dissolve
    hide maya with dissolve
    show leo neutral at vn_right with dissolve
    show mc neutral at vn_left with dissolve

    call screen prologue_action_choice

    # MC bicara — MC kiri, Leo kanan
    player "Rencana itu masuk akal, Leo. Dengan bimbinganmu, kita jadi tahu materi apa yang harus dipelajari setiap hari."

    # Leo bicara — sudah di kanan
    leo "Bagus. [player_name], kamu jadi koordinator kelompok. Pastikan semua hadir, catat hasil latihan, dan beri tahu aku materi mana yang masih sulit dipahami."

    # MC bicara
    player "Siap, Leo. Aku akan memastikan semuanya mengikuti jadwal. Kita pasti bisa menembus skor 400!"

    # Bima bicara — tambahkan Bima di tengah
    show bima neutral at vn_center with dissolve
    bima "Co-op Study Group Accepted! Besok kita mulai grinding soal sampai semuanya naik level!"

    # Leo bicara — MC kiri, Bima tengah, Leo kanan
    leo "Sebut saja belajar. Besok pagi kita mulai dari Vocabulary. Jangan ada yang terlambat."

    # Maya masuk sebagai koordinator — semua keluar, Maya di tengah
    hide mc with dissolve
    hide bima with dissolve
    hide leo with dissolve
    show maya neutral at vn_center with dissolve
    maya "Kalau begitu, aku buat grup WhatsApp khusus Study Group kita, ya. Jadwal, materi dari Leo, dan hasil latihan bisa kita bagikan di sana supaya semuanya tetap terkoordinasi."

    # Rina bicara — tambahkan Rina di kiri
    show rina neutral at vn_left with dissolve
    rina "Setuju! Kalau ada perubahan jadwal atau ada yang belum paham materi, kita bisa langsung diskusi di grup."

    # Reza bicara — ganti Rina di kiri dengan Reza
    hide rina with dissolve
    show reza neutral at vn_left with dissolve
    reza "Boleh, tapi nama grupnya apa? Jangan terlalu formal sampai rasanya kayak grup pengumuman kampus."

    # Bima bicara — tambahkan Bima di kanan
    show bima neutral at vn_right with dissolve
    bima "Gimana kalau namanya 'TOEFL Raid Party: Road to Level 400'? Kedengarannya keren, kan?"

    # Maya bicara — Reza kiri, Maya tengah, Bima kanan
    maya "Keren menurutmu sendiri. Kita butuh nama yang pendek dan gampang dicari."

    # MC bicara — ganti Reza di kiri dengan MC
    hide reza with dissolve
    show mc neutral at vn_left with dissolve
    player "Bagaimana kalau 'Seven Days to TOEFL'? Sesuai dengan waktu belajar kita yang cuma tujuh hari."

    # Rina bicara — ganti Bima di kanan dengan Rina
    hide bima with dissolve
    show rina neutral at vn_right with dissolve
    rina "Aku suka! Sederhana, tapi langsung mengingatkan kita sama target minggu ini."

    # Leo bicara — tambahkan Leo, geser posisi: MC kiri, Maya tengah, Leo kanan
    hide rina with dissolve
    show leo neutral at vn_right with dissolve
    leo "Boleh. Gunakan grup itu hanya untuk jadwal, materi, pertanyaan, dan hasil latihan. Jangan kirim meme atau spam saat sesi belajar berlangsung."

    # Bima bicara — ganti MC di kiri dengan Bima
    hide mc with dissolve
    show bima neutral at vn_left with dissolve
    bima "Baik, Pak Guru. Meme hanya boleh dikirim setelah jam belajar."

    # Maya bicara — Bima kiri, Maya tengah, Leo kanan
    maya "Sip, nama grup sudah diputuskan. Aku buat grupnya sekarang. Rina, bantu tambahkan anggota lain, ya. Nanti aku jadikan kamu dan [player_name] sebagai admin supaya koordinasinya lebih mudah."
    
    play sound audio.sfx_notification
    system "TING! Ponsel mereka berbunyi hampir bersamaan. Grup WhatsApp 'Seven Days to TOEFL' resmi dibuat."
    call screen whatsapp_group_setup

    maya "Nah, grupnya sudah jadi. Nanti malam kita bahas di sana soal jam dan tempat berkumpul untuk sesi pertama, ya."
    rina "Setuju. Kita kirim jadwal kosong masing-masing, biar nggak ada yang tiba-tiba bilang bentrok setelah waktunya diputuskan."
    reza "Kalau bisa jangan terlalu pagi. Otakku biasanya belum selesai loading sebelum jam delapan."
    bima "Aku fleksibel, selama tempatnya punya colokan, Wi-Fi, dan sinyal yang bagus. Itu kebutuhan belajar yang sangat penting."
    leo "Kirim waktu kosong kalian ke grup sebelum jam sembilan malam. Setelah semuanya menjawab, aku tentukan jadwal dan tempat yang paling memungkinkan."
    player "Baik. Nanti aku bantu merekap jawaban semuanya di grup supaya kita bisa segera memastikan jadwal."
    maya "Sip! Berarti urusan waktu dan tempat kita lanjutkan di grup nanti malam. Jangan ada yang cuma membaca tanpa membalas."

    scene bg black with fade
    centered "{size=46}MALAM HARI{/size}\n{size=28}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "Setelah perjalanan pulang, [player_name] akhirnya tiba di kamar dan meletakkan barang-barangnya."
    player "Akhirnya sampai juga. Sebelum tidur, aku harus mengecek grup dan membantu merekap jadwal belajar untuk besok."

    with hpunch
    play sound audio.sfx_notification
    call screen whatsapp_evening_notification
    player "Baru beberapa menit dibuat, grup ini sudah lebih aktif daripada grup tugas satu semester."
    call screen whatsapp_evening_chat
    player "Jadwal sudah direkap. Sekarang tinggal berdoa Reza dan Bima datang dalam keadaan sadar penuh."

    $ target_score = 400
    $ study_calendar_unlocked = True

    scene bg black with fade
    call screen study_plan_ready
    system "Prolog selesai. Besok pagi, Leo akan memulai sesi belajar pertama bersama kelompok."
    system "Tujuh hari belajar menuju target skor 400 resmi dimulai."
    jump day_0_ending_calendar


label day_0_ending_calendar:
    call screen study_calendar_transition
    $ calendar_completed_day = 0
    $ calendar_resume_label = "day_0_ending_calendar"
    $ calendar_continue_label = "day_1_morning"
    jump process_study_calendar


label day_1_morning:
    $ day = 1
    $ day_1_status = "not_started"
    $ day_1_vocab_score = 0
    $ day_1_summary_seen = False
    $ day_1_group_reply = ""

    scene bg black with fade
    centered "{size=50}HARI PERTAMA{/size}\n{size=30}Vocabulary Dasar{/size}"

    scene bg player bedroom morning with fade
    play music audio.bgm_campus loop fadein 0.5
    show mc neutral at vn_center with dissolve
    system "Sabtu, pukul 06.45. Cahaya pagi mulai masuk melalui celah tirai kamar [player_name]."

    with hpunch
    system "TRIING! TRIING! TRIING!"
    player "Ugh... alarmnya terdengar seperti sedang menagih utang."
    system "[player_name] meraih ponsel di samping bantal dan mematikan alarm untuk ketiga kalinya."
    player "Sesi pertama dimulai pukul delapan di perpustakaan kampus."
    player "Kasur ini menyuruhku tetap tinggal, tapi pesan Leo semalam rasanya sedang menatapku dari layar ponsel."

    $ day_1_choice = renpy.call_screen("day_one_morning_choice")

    if day_1_choice == "skip":
        jump day_1_skip

    jump day_1_prepare


label day_1_skip:
    $ day_1_status = "skipped"
    $ day_1_makeup_pending = True

    player "Sepertinya hari ini aku benar-benar tidak sanggup. Badanku terasa kurang fit dan kepalaku sedikit pusing."
    player "Aku harus memberi tahu mereka. Menghilang tanpa kabar justru akan membuat semuanya khawatir."
    system "[player_name] membuka grup WhatsApp Seven Days to TOEFL dan mulai mengetik permohonan maaf."

    call screen whatsapp_day_one_skip_chat

    player "Syukurlah mereka mengerti. Meski begitu, rasanya tetap tidak enak melewatkan sesi pertama."
    system "[player_name] kembali beristirahat. Sementara itu, sesi belajar di perpustakaan tetap berlangsung."

    scene bg black with fade
    centered "{size=44}SORE HARI{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "Saat kondisi [player_name] mulai membaik, sejumlah foto catatan dan latihan masuk ke grup."
    player "Rina mengirim catatan lengkap, Maya membuat ringkasan, dan Leo memberi tanda pada soal yang harus kukerjakan."
    player "Sementara Bima... mengirim foto Reza tertidur di atas kamus."
    player "Sepertinya aku melewatkan materi penting sekaligus tontonan langka."
    player "Hari ini sudah terlewat. Malam ini aku akan membaca catatan mereka supaya besok tidak semakin tertinggal."

    jump day_1_evening_group_chat


label day_1_prepare:
    $ day_1_status = "in_progress"
    $ day_1_makeup_pending = False

    player "Tidak. Kalau menyerah pada kasur sekarang, rencana tujuh hari ini bisa berakhir sebelum benar-benar dimulai."
    player "Ayo bangun. Mandi, sarapan, lalu berangkat."
    player "Buku catatan, alat tulis, ponsel, dan semangat hidup... lengkap."
    system "Beberapa menit kemudian, [player_name] sudah bersiap sambil menghabiskan sarapan sederhana."
    player "Semoga semangat hidup Reza juga sudah selesai loading."

    scene bg black with fade
    centered "{size=44}PUKUL 07.50{/size}\n{size=27}Kampus FTI UNIBBA{/size}"

    scene bg campus morning with fade
    play music audio.bgm_campus loop fadein 0.5
    show mc neutral at vn_center with dissolve
    system "[player_name] tiba di kampus sepuluh menit lebih awal lalu berjalan menuju ruang belajar perpustakaan."
    player "Udara pagi ternyata lumayan menyegarkan. Untung aku tidak memilih kembali tidur."

    scene bg library study with fade
    play music audio.bgm_study loop fadein 0.5
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Pagi, [player_name]! Aku datang tiga puluh menit lebih awal karena takut terlambat."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Dia datang saat petugas perpustakaan baru selesai membuka tirai."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Setidaknya kita tidak perlu khawatir Rina terlambat."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Pagi... tubuhku berhasil datang tepat waktu. Kesadaranku masih mencari tempat parkir."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Party hampir lengkap! Tutor kita belum login?"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Aku sudah di sini sejak sepuluh menit lalu."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Kenapa kemunculanmu selalu seperti karakter rahasia?"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Karena kalian terlalu sibuk berbicara. Duduk. Kita mulai."

    hide normal_speaker with day_one_speaker_swap
    scene bg library study with dissolve
    system "Mereka duduk mengelilingi meja. Leo membuka catatan dan berdiri di dekat papan tulis."

    show screen vocabulary_lesson_board("concept")
    show screen day_one_speaker_portrait("leo")
    leo "Hari pertama kita mulai dengan Vocabulary dasar."
    leo "Pada soal kosakata di bagian Reading TOEFL, yang dicari adalah makna paling dekat dalam konteks, bukan selalu arti pertama yang muncul di kamus."
    show screen day_one_speaker_portrait("rina")
    rina "Jadi kalau ada satu kata yang tidak kukenal, aku tidak perlu langsung panik?"
    show screen day_one_speaker_portrait("leo")
    leo "Benar. Kalian tidak perlu menghafal seluruh kamus. Baca kalimat dan bagian paragraf di sekitarnya, lalu cari bukti yang menjelaskan kata itu."
    show screen day_one_speaker_portrait("reza")
    reza "Berarti jangan langsung error hanya karena menemukan satu variabel asing."
    show screen day_one_speaker_portrait("leo")
    leo "Perumpamaanmu aneh, tapi benar."

    hide screen vocabulary_lesson_board
    show screen vocabulary_lesson_board("steps")
    show screen day_one_speaker_portrait("leo")
    leo "Gunakan empat langkah di papan. Pertama, baca konteks. Kedua, tandai petunjuk. Ketiga, prediksi maknanya sebelum melihat pilihan. Terakhir, parafrasekan bagian kalimat dengan pilihanmu, lalu baca ulang."
    show screen day_one_speaker_portrait("maya")
    maya "Jadi kita tidak langsung berburu jawaban yang kelihatannya paling familiar."
    show screen day_one_speaker_portrait("leo")
    leo "Tepat. Pilihan yang terdengar familiar tetap salah kalau tidak cocok dengan isi kalimat atau jenis katanya."
    show screen day_one_speaker_portrait("player")
    player "Berarti jawaban harus cocok maknanya dan kalimat hasil parafrasanya tetap masuk akal."
    show screen day_one_speaker_portrait("leo")
    leo "Benar. Itu kebiasaan sederhana yang mencegah banyak jawaban terburu-buru."

    hide screen vocabulary_lesson_board
    show screen vocabulary_lesson_board("clues")
    show screen day_one_speaker_portrait("leo")
    leo "Petunjuk konteks memiliki beberapa bentuk. Definisi dan contoh biasanya menjelaskan langsung, sedangkan kata seperti but, unlike, atau however menunjukkan kontras."
    leo "Hubungan sebab dan hasil juga penting. Kalau suatu kejadian membuat tokohnya meminta penjelasan, misalnya, kata sebelumnya mungkin berarti membingungkan atau tidak jelas."
    show screen day_one_speaker_portrait("rina")
    rina "Berarti kata penghubung kecil justru bisa menjadi petunjuk besar."
    show screen day_one_speaker_portrait("leo")
    leo "Betul. Kalian juga boleh memakai imbuhan sebagai petunjuk tambahan: un- biasanya berarti tidak atau kebalikan, re- berarti lagi atau kembali, mis- berarti salah, dan -less berarti tanpa."
    show screen day_one_speaker_portrait("bima")
    bima "Jadi misunderstood artinya memahami dengan build yang salah?"
    show screen day_one_speaker_portrait("maya")
    maya "Atau memahami secara keliru karena tidak membaca instruksi."
    show screen day_one_speaker_portrait("leo")
    leo "Definisi Maya lebih layak masuk catatan. Ingat, imbuhan membantu, tetapi konteks tetap menjadi bukti utama."

    hide screen vocabulary_lesson_board
    show screen vocabulary_lesson_board("example")
    show screen day_one_speaker_portrait("leo")
    leo "Sekarang perhatikan contoh di papan: Unlike his outgoing sister, Arman is reserved and rarely speaks in class."
    leo "Kata unlike memberi tanda bahwa Arman berlawanan dengan saudara perempuannya yang outgoing. Frasa rarely speaks memperkuat petunjuk itu."
    show screen day_one_speaker_portrait("player")
    player "Jadi reserved paling dekat artinya quiet atau pendiam."
    show screen day_one_speaker_portrait("rina")
    rina "Kita bisa menyimpulkannya meski sebelumnya belum tahu arti reserved."
    show screen day_one_speaker_portrait("leo")
    leo "Tepat. Kalian membaca hubungan antarbagian kalimat, bukan menebak satu kata secara terpisah."
    show screen day_one_speaker_portrait("bima")
    bima "Untung Arman pendiam. Kalau dia ikut party kita, contoh kalimatnya pasti terlalu ramai."
    show screen day_one_speaker_portrait("maya")
    maya "Contohnya tidak ramai. Kamu yang ramai."

    hide screen vocabulary_lesson_board
    show screen vocabulary_lesson_board("checklist")
    show screen day_one_speaker_portrait("leo")
    leo "Sebelum menjawab, periksa tiga hal di papan: dukungan konteks, kesesuaian jenis kata, dan apakah kalimat tetap masuk akal setelah bagian itu diparafrasekan."
    leo "Urutannya sederhana: baca, cari petunjuk, lalu uji makna. Kecepatan akan datang setelah kalian terbiasa."
    show screen day_one_speaker_portrait("player")
    player "Baik. Aku akan mencoba mengikuti urutan itu, bukan sekadar mengandalkan tebakan pertama."
    show screen day_one_speaker_portrait("leo")
    leo "Sekarang giliranmu, [player_name]. Jawab lima soal pendek ini. Setiap jawaban benar bernilai sepuluh poin."

    hide screen vocabulary_lesson_board
    hide screen day_one_speaker_portrait

    call screen day_one_vocab_quiz(
        1,
        "The two buildings are adjacent; they stand directly beside each other.\n\nApa arti kata adjacent?",
        "Identical",
        "Next to each other",
        "Far apart"
    )
    $ vocab_answer = _return
    $ vocab_correct = vocab_answer == "b"

    if vocab_correct:
        $ day_1_vocab_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Adjacent berarti berada tepat di sebelah satu sama lain."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Frasa directly beside each other memberikan definisinya."
    elif vocab_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Adjacent berarti identik?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Belum tepat. Tidak ada petunjuk bahwa bangunannya sama. Adjacent berarti saling bersebelahan."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Adjacent berarti berjauhan?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Kebalikannya. Frasa directly beside each other berarti kedua bangunan itu saling bersebelahan."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih B, next to each other. Frasa directly beside each other menjelaskan artinya secara langsung."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "B juga. Bagian setelah titik koma seperti komentar dalam kode; tugasnya menjelaskan bagian sebelumnya."

    hide normal_speaker with day_one_speaker_swap
    if vocab_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_1_vocab_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_1_vocab_score]/50."

    call screen day_one_vocab_quiz(
        2,
        "Unlike the temporary shelters, the new clinic is permanent and will remain open for many years.\n\nApa arti kata temporary?",
        "Expensive",
        "Permanent",
        "Lasting for a short time"
    )
    $ vocab_answer = _return
    $ vocab_correct = vocab_answer == "c"

    if vocab_correct:
        $ day_1_vocab_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Temporary berarti berlangsung untuk waktu singkat atau sementara."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Unlike mengontraskan temporary dengan permanent."
    elif vocab_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Temporary berarti mahal?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Tidak ada petunjuk tentang harga. Kata permanent menjadi lawan maknanya, jadi temporary berarti sementara."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Temporary berarti permanen?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Kalimat memakai unlike untuk menunjukkan pertentangan. Temporary justru berarti berlangsung sementara."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Jawabanku C. Unlike menunjukkan kontras antara temporary dan permanent."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "C juga. Temporary itu versi limited-time, sedangkan kliniknya akan bertahan bertahun-tahun."

    hide normal_speaker with day_one_speaker_swap
    if vocab_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_1_vocab_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_1_vocab_score]/50."

    call screen day_one_vocab_quiz(
        3,
        "The instructions were ambiguous, so the students asked the teacher to explain them more clearly.\n\nApa arti kata ambiguous?",
        "Unclear",
        "Detailed",
        "Familiar"
    )
    $ vocab_answer = _return
    $ vocab_correct = vocab_answer == "a"

    if vocab_correct:
        $ day_1_vocab_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Ambiguous berarti tidak jelas atau memiliki makna yang membingungkan."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Para siswa meminta penjelasan yang lebih jelas karena instruksinya ambiguous."
    elif vocab_answer == "b":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Ambiguous berarti terperinci?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Kalau instruksinya terperinci, mereka tidak perlu meminta penjelasan lebih jelas. Ambiguous berarti tidak jelas."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Ambiguous berarti sudah dikenal?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Bukan. Hubungan sebab dan hasil pada kalimat menunjukkan bahwa ambiguous berarti tidak jelas."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih A, unclear. Kalau instruksinya sudah jelas, para siswa tidak perlu meminta penjelasan lagi."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "A juga. Kalau sebuah instruksi membuat semua orang meminta klarifikasi, berarti dokumentasinya jelas belum jelas."

    hide normal_speaker with day_one_speaker_swap
    if vocab_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_1_vocab_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_1_vocab_score]/50."

    call screen day_one_vocab_quiz(
        4,
        "Many nocturnal animals, such as bats and owls, search for food at night.\n\nApa arti kata nocturnal?",
        "Living underground",
        "Eating only plants",
        "Active at night"
    )
    $ vocab_answer = _return
    $ vocab_correct = vocab_answer == "c"

    if vocab_correct:
        $ day_1_vocab_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Nocturnal berarti aktif pada malam hari."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Kelelawar, burung hantu, dan frasa at night menjadi petunjuknya."
    elif vocab_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Nocturnal berarti hidup di bawah tanah?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Tidak semua hewan dalam contoh hidup di bawah tanah. Frasa at night menunjukkan bahwa nocturnal berarti aktif pada malam hari."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Nocturnal berarti hanya memakan tumbuhan?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Kalimat tidak membahas jenis makanan. Petunjuk utamanya adalah search for food at night."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Jawabanku C! Kelelawar dan burung hantu mencari makanan pada malam hari; mereka anggota party shift malam."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aku juga memilih C. Contohnya membantu, tetapi frasa at night yang memastikan artinya aktif pada malam hari."

    hide normal_speaker with day_one_speaker_swap
    if vocab_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_1_vocab_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_1_vocab_score]/50."

    call screen day_one_vocab_quiz(
        5,
        "Riko misinterpreted the schedule and arrived on Tuesday instead of Thursday.\n\nApa arti kata misinterpreted?",
        "Announced publicly",
        "Understood incorrectly",
        "Followed carefully"
    )
    $ vocab_answer = _return
    $ vocab_correct = vocab_answer == "b"

    if vocab_correct:
        $ day_1_vocab_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Misinterpreted berarti memahami dengan keliru."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Awalan mis- dan hari kedatangannya yang salah sama-sama mendukung makna itu."
    elif vocab_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Misinterpreted berarti mengumumkan kepada orang banyak?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Tidak. Riko datang pada hari yang salah karena ia memahami jadwal dengan keliru."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Misinterpreted berarti mengikuti dengan teliti?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Hasil tindakannya menunjukkan kebalikannya. Ia memahami jadwal secara keliru."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku memilih B. Riko membaca jadwal, tetapi datang pada hari yang salah. Berarti ia memahaminya secara keliru."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "B juga. Awalan mis- menunjukkan kesalahan, lalu jadwal yang meleset menjadi bukti kegagalan quest-nya."

    hide normal_speaker with day_one_speaker_swap
    if vocab_correct:
        system "Jawaban benar! +10 poin. Skor akhir: [day_1_vocab_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor akhir: [day_1_vocab_score]/50."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Tumben, kali ini bukan aku yang dijadikan contoh orang yang salah memahami jadwal."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Sesekali orang lain juga harus mendapat giliran menjadi contoh buruk."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Perkembangan metode mengajarnya mengkhawatirkan, tapi efektif."

    hide normal_speaker with day_one_speaker_swap

    if 1 not in extra_practice_days:
        call screen extra_study_quiz(
            1,
            "VOCABULARY BONUS",
            "The library extended its opening hours during exam week, so students had more time to study.\n\nApa arti kata extended?",
            "Shortened",
            "Made longer",
            "Moved to another place",
            day_1_vocab_score,
            "Gunakan hubungan sebab-akibat: jam buka memberi lebih banyak waktu belajar."
        )
        $ extra_answer = _return
        if extra_answer == "b":
            $ extra_practice_score += 10
            system "Jawaban bonus benar! +10 poin tambahan."
        else:
            system "Jawaban bonus belum tepat. Ingat petunjuk konteks tentang waktu yang menjadi lebih panjang."
        $ extra_practice_days.append(1)

    system "Skor latihan Vocabulary Hari 1: [day_1_vocab_score] dari 50 poin. Bonus kumulatif: [extra_practice_score]."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    if day_1_vocab_score == 50:
        leo "Lima jawaban benar. Sempurna, [player_name]. Kamu sudah membaca konteks dan menguji setiap makna dengan teliti."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Koordinator kita langsung mendapat nilai sempurna!"
        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Carry terdeteksi."
    elif day_1_vocab_score >= 40:
        leo "Empat jawaban benar. Dasarnya sudah sangat bagus. Periksa satu petunjuk yang terlewat, lalu lanjutkan."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Lumayan. Belum waktunya sombong, tapi juga jelas bukan waktunya panik."
    elif day_1_vocab_score >= 30:
        leo "Tiga jawaban benar. Strategimu sudah berjalan, tetapi kamu masih perlu menguji kembali jawaban sebelum memilih."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Kita latihan lagi bersama nanti, [player_name]."
    elif day_1_vocab_score >= 20:
        leo "Dua jawaban benar. Jangan terpaku pada kata asing; cari hubungan antarkata dan bukti paling dekat."
        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Bagus. Bug-nya sudah ditemukan. Tinggal diperbaiki."
    else:
        leo "Skornya masih rendah, tetapi sekarang kamu sudah mengetahui cara menemukan jawabannya. Kita akan mengulang strategi ini sampai terasa alami."
        leo "Tujuan latihan pertama bukan nilai sempurna, melainkan mengenali pola kesalahan sebelum ujian."
        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Bagus. Berarti bug-nya sudah ditemukan. Tinggal diperbaiki."

    hide normal_speaker with day_one_speaker_swap
    scene bg library study with dissolve
    system "Setelah hampir satu jam, Leo memberi waktu istirahat selama lima belas menit."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku selalu tertukar antara desert dan dessert."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Dessert punya dua huruf s karena kita selalu ingin tambah satu porsi."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Itu metode ilmiah pertama yang langsung kupahami."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Tidak ilmiah. Tapi kalau membuat kalian mengingatnya, silakan."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Kalau aku menutup mata lima menit, itu termasuk cara mempertahankan energi, kan?"
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Kalau dengkuranmu muncul, namanya shutdown."
    hide normal_speaker with day_one_speaker_swap
    system "Beberapa detik kemudian, kepala Reza benar-benar turun perlahan ke atas bukunya."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Reza disconnect!"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Biarkan dua menit. Setelah itu bangunkan. Kita masih punya latihan membuat kalimat."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku masih mendengar... sebagian."

    hide normal_speaker with day_one_speaker_swap
    scene bg library study with dissolve
    system "Setelah istirahat, setiap anggota diminta membuat satu kalimat menggunakan kosakata yang baru dipelajari."
    system "Sebagai pengayaan, Leo menambahkan require, frequently, essential, dan retain ke daftar kosakata mereka, lengkap dengan contoh penggunaannya."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "The TOEFL test requires consistent practice."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Bagus. Require berarti membutuhkan, dan kamu menggunakan requires dengan tepat karena subjeknya tunggal."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "A bug frequently appears when the deadline is near."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Itu Vocabulary atau curhat?"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Keduanya. Kalimatnya benar."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Sleep is essential for gamers."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Benar. Sekarang coba praktikkan juga, bukan hanya dijadikan contoh kalimat."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku merasa diserang secara akademis."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Reviewing notes helps me retain new words."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Bagus. Mengulang sedikit setiap hari lebih efektif daripada menghafal banyak kata sekaligus."

    hide normal_speaker with day_one_speaker_swap
    system "Selama hampir dua jam berikutnya, mereka menyusun kartu kata, berlatih berpasangan, dan membahas kesalahan satu per satu."
    system "Pukul 11.20, Leo menutup sesi dan membagikan daftar kosakata untuk latihan mandiri."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Hari ini cukup. Pelajari kembali lima kata utama dari kuis dan buat satu kalimat untuk setiap kata."
    leo "Besok kita masuk ke Structure dasar. Kita akan mencari subjek, verba, dan pola kalimat yang benar."
    leo "Malam ini aku akan memeriksa ringkasan Maya dan mengirim versi akhirnya ke grup."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Drafnya akan kurapikan dulu sebelum diperiksa Leo."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku juga kirim foto catatan dan jawaban latihan."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku akan mempelajarinya setelah otakku selesai reboot."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Day One cleared! Party memperoleh skill baru: Context Clue!"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Kita memperoleh tugas rumah."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Nama skill itu jauh kurang menarik."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Terima kasih, Leo. Sekarang aku tahu satu kata asing tidak selalu membuat seluruh kalimat mustahil dipahami."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Itu inti pelajaran hari ini. Sampai besok, dan tetap datang tepat waktu."

    hide screen vocabulary_lesson_board
    hide normal_speaker with day_one_speaker_swap
    scene bg black with fade
    centered "{size=44}SORE HARI{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "Sore hari, [player_name] kembali ke rumah dan membuka catatan dari sesi pertama."
    player "Adjacent, temporary, ambiguous, nocturnal, misinterpreted... Lima kata saja sudah punya cerita sendiri."
    player "Masih ada banyak yang harus dipelajari, tapi hari pertama ternyata tidak semenakutkan bayanganku."
    player "Besok giliran Structure. Sebelum tidur, aku akan memasang alarm dan menunggu ringkasan yang dijanjikan Leo."

    jump day_1_evening_group_chat


label day_1_evening_group_chat:
    play music audio.bgm_main_menu loop fadein 0.5
    scene bg black with fade
    centered "{size=44}PUKUL 21.47{/size}\n{size=26}Kamar [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve

    if day_1_status == "skipped":
        system "Setelah membaca catatan susulan dari teman-temannya, [player_name] bersiap meletakkan ponsel dan beristirahat."
    else:
        system "Setelah mengulang lima kosakata dari sesi pagi, [player_name] bersiap meletakkan ponsel dan beristirahat."

    with hpunch
    system "BZZT! Sebuah notifikasi baru dari grup Seven Days to TOEFL muncul."
    call screen whatsapp_day_one_summary_notification

    player "Sepertinya ringkasan dari Leo sudah dikirim. Aku baca sebentar sebelum tidur."
    $ day_1_group_reply = renpy.call_screen("whatsapp_day_one_summary_chat")
    call screen whatsapp_day_one_summary_followup(day_1_group_reply)
    $ day_1_summary_seen = True

    if day_1_status == "skipped":
        player "Ringkasan ini akan sangat membantu mengejar materi yang kulewatkan hari ini."
    else:
        player "Ringkasan Leo membuat pembahasan tadi terasa jauh lebih mudah diingat."

    player "Alarm pukul 06.30 sudah terpasang. Sekarang benar-benar waktunya istirahat."
    system "[player_name] mengisi daya ponsel, mematikan lampu, lalu berbaring untuk menutup Hari 1."

    if day_1_status == "in_progress":
        $ day_1_status = "completed"

    jump day_1_ending


label day_1_ending:
    menu day_1_night_menu:
        "Sebelum tidur, apa yang ingin kamu lakukan?"

        "Simpan Permainan":
            $ ShowMenu('save')()
            jump day_1_night_menu

        "Tidur (Lanjut ke Hari 2)":
            pass

    scene bg black with fade

    if day_1_status == "skipped":
        system "Hari pertama telah berlalu. Latihan Vocabulary susulan masih menunggu [player_name]."
    else:
        system "Hari pertama selesai. Kosakata dasar dan strategi memperkirakan makna melalui konteks telah dipelajari."

label day_1_ending_calendar:
    call screen study_calendar_day_one_to_two(skipped=(day_1_status == "skipped"))
    $ calendar_completed_day = 1
    $ calendar_resume_label = "day_1_ending_calendar"
    $ calendar_continue_label = "day_2_morning"
    jump process_study_calendar


label day_2_morning:
    play music audio.bgm_campus loop fadein 0.5
    $ day = 2
    $ day_2_choice = ""
    $ day_2_status = "not_started"
    $ day_2_makeup_pending = False
    $ day_2_structure_score = 0
    $ day_2_summary_seen = False
    $ day_2_group_reply = ""

    scene bg black with fade
    centered "{size=50}HARI KEDUA{/size}\n{size=30}Structure Dasar{/size}"

    scene bg player bedroom morning with fade
    show mc neutral at vn_center with dissolve
    system "Minggu, pukul 06.30. Alarm yang dipasang [player_name] semalam berbunyi tepat waktu."

    with hpunch
    system "TRIING! TRIING! TRIING!"
    player "Alarmnya berhasil. Sekarang tinggal memastikan pemiliknya ikut bangun."
    system "[player_name] duduk di tepi tempat tidur, mematikan alarm, lalu meraih ponsel."

    with hpunch
    system "BZZT! Beberapa pesan baru masuk ke grup Seven Days to TOEFL."
    call screen whatsapp_day_two_confirmation_chat

    player "Pukul delapan, ruang belajar perpustakaan, meja dekat jendela. Hari ini materinya Structure dasar."

    if day_1_status == "skipped":
        player "Kemarin aku sudah tertinggal Vocabulary. Kalau melewatkan hari ini juga, latihan susulanku akan semakin menumpuk."
    else:
        player "Tugas Vocabulary sudah selesai. Tinggal menjaga ritme belajar hari ini."

    $ day_2_choice = renpy.call_screen("day_two_morning_choice")

    if day_2_choice == "skip":
        jump day_2_skip

    jump day_2_prepare


label day_2_skip:
    $ day_2_status = "skipped"
    $ day_2_makeup_pending = True

    player "Aku sebenarnya ingin berangkat, tapi ada urusan keluarga pagi ini yang tidak bisa ditinggalkan."

    if day_1_status == "skipped":
        player "Ini akan menjadi dua sesi yang kulewatkan berturut-turut. Rasanya tidak enak, tetapi aku tetap harus memberi kabar dengan jujur."
    else:
        player "Aku tidak boleh menghilang begitu saja. Sebagai koordinator, setidaknya aku harus memberi kabar yang jelas."

    player "Lebih baik kukirim izin sekarang sebelum mereka mulai belajar."
    system "[player_name] membuka grup dan mulai mengetik."

    call screen whatsapp_day_two_skip_chat

    if day_1_status == "skipped":
        player "Dua latihan susulan bukan beban kecil. Malam ini aku harus mulai mengejar Vocabulary dan Structure satu per satu."
    else:
        player "Mereka sudah membantu menyiapkan catatan. Malam ini aku harus benar-benar mengerjakan latihan susulannya."

    system "[player_name] meletakkan ponsel dan menyelesaikan urusan keluarga yang membuatnya tetap berada di rumah."

    scene bg black with fade
    centered "{size=44}MENJELANG SIANG{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom morning with fade
    show mc neutral at vn_center with dissolve
    system "Menjelang siang, urusan itu akhirnya selesai. Foto papan tulis, catatan, dan lembar latihan mulai masuk ke grup."
    player "Rina benar-benar menandai semua subjek dan verba. Catatan Maya juga jauh lebih ramah daripada hutan rumus."
    player "Aku memang melewatkan sesi hari ini, tapi bukan berarti materinya boleh kulewatkan juga."
    system "Hari 2 ditandai sebagai dilewati. Latihan Structure susulan telah ditambahkan."

    jump day_2_evening_group_chat


label day_2_prepare:
    play music audio.bgm_study loop fadein 0.5
    $ day_2_status = "in_progress"
    $ day_2_makeup_pending = False

    if day_1_status == "skipped":
        player "Kemarin aku sudah tertinggal Vocabulary. Hari ini aku tidak boleh menambah utang materi."
    else:
        player "Kalau tetap memeluk bantal, subject dan verb akan datang menghantuiku dalam mimpi."

    player "Ayo bersiap. Aku masih punya cukup waktu untuk sarapan dan berangkat."
    system "[player_name] mandi, berpakaian, lalu memeriksa isi tas sebelum meninggalkan kamar."

    if day_1_status == "skipped":
        system "Latihan susulan Vocabulary dan catatan yang dikirim teman-temannya dimasukkan ke dalam tas."
    else:
        system "Tugas Vocabulary, buku catatan, dan alat tulis sudah tersimpan rapi di dalam tas."

    player "Semua lengkap. Kali ini aku berangkat sebelum grup mengirim tim pencarian."

    scene bg black with fade
    centered "{size=44}PUKUL 07.50{/size}\n{size=27}Perpustakaan Kampus{/size}"

    scene bg library study with fade
    system "[player_name] memasuki ruang belajar yang sama dan menemukan beberapa anggota kelompok sudah menunggu."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Pagi, [player_name]! Hari ini aku hanya datang dua puluh menit lebih awal."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Kemajuan besar. Kemarin tiga puluh menit, sekarang tinggal dua puluh."

    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Pelan-pelan, Rina sedang belajar menjadi manusia yang datang pada waktu normal."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Pagi. Aku membawa tugas, kopi, dan kesadaran secukupnya."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Mana yang paling penting?"

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Kopinya. Dua yang lain bergantung padanya."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Pukul 07.59! Party member terakhir berhasil login sebelum batas waktu!"

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Kamu datang dengan sisa satu menit. Itu bukan pencapaian."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Untuk rekam jejakku, ini personal best."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Sayangnya dia benar."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Berarti semuanya sudah lengkap."

    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Study Group Hari 2 siap dimulai."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Bagus. Senyapkan ponsel dan keluarkan catatan kalian."

    hide normal_speaker with day_one_speaker_swap
    system "Jam menunjukkan tepat pukul 08.00. Leo berdiri di depan papan tulis sementara anggota lain mengambil tempat."

    jump day_2_structure_lesson


label day_2_structure_lesson:
    play music audio.bgm_study loop fadein 0.5
    scene bg library study with dissolve

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Hari ini kita belajar Structure dasar. Kita mulai dengan mengenali subjek dan verba dalam sebuah kalimat."
    leo "Dalam klausa deklaratif dasar yang kita pelajari, kita membutuhkan subjek dan finite verb. Setelah menemukan keduanya, barulah kita memeriksa apakah polanya masuk akal."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Jadi sebelum memikirkan pilihan jawaban, kita cari dulu siapa atau apa yang dibicarakan dan apa yang dilakukannya?"

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Tepat. Subjek menunjukkan pelaku atau topik, sedangkan verba menunjukkan tindakan atau keadaan."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Berarti dalam kalimat 'Bima arrives on time', Bima subjeknya dan arrives bukti kejadian langka?"

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Secara tata bahasa benar. Secara fakta masih perlu penelitian lebih lanjut."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Setidaknya hari ini datanya mendukung. Dia datang satu menit sebelum mulai."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Contohnya bisa dipakai."

    if day_1_status == "skipped":
        leo "[player_name], catatan Vocabulary susulan sudah kutaruh di bagian depan. Fokus dulu pada sesi hari ini; setelah selesai, kita atur waktu untuk mengejar materi kemarin."
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Baik. Aku akan menyelesaikan keduanya tanpa mencampur semua catatan menjadi satu bencana."
    else:
        leo "Sebelum mulai, kumpulkan lima kalimat tugas Vocabulary kalian. Aku akan memeriksanya saat waktu istirahat."
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Sudah lengkap. Lima kata itu akhirnya punya kalimat masing-masing."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Sekarang buka halaman pertama. Kita tandai subject dan verb sebelum masuk ke latihan."

    hide normal_speaker with day_one_speaker_swap
    system "Sesi Structure Hari 2 resmi dimulai."

    show screen structure_lesson_board("core")
    show screen day_one_speaker_portrait("leo")
    leo "Pada bagian Structure, jangan langsung menilai seluruh kalimat. Cari rangkanya lebih dahulu."
    leo "Dalam pola dasar hari ini, rangka minimum sebuah klausa adalah subject dan finite verb. Finite verb membawa tense atau agreement; dalam verb phrase, biasanya elemen pertama yang bersifat finite."

    show screen day_one_speaker_portrait("rina")
    rina "Kalau kalimatnya panjang, berarti kita tetap mencari dua bagian utama itu dulu?"

    show screen day_one_speaker_portrait("leo")
    leo "Benar. Subject menunjukkan siapa atau apa yang dibicarakan, sedangkan verb menunjukkan tindakan atau keadaan subject tersebut."

    show screen day_one_speaker_portrait("bima")
    bima "Jadi kita mencari karakter utama dan aksinya."

    show screen day_one_speaker_portrait("maya")
    maya "Untuk pertama kalinya, penjelasan versi gim-mu tidak merusak materi."

    show screen day_one_speaker_portrait("leo")
    leo "Boleh memakai perumpamaan itu selama kalian tetap memeriksa bentuk verbanya."

    hide screen structure_lesson_board
    show screen structure_lesson_board("main_pair")
    show screen day_one_speaker_portrait("leo")
    leo "Perhatikan kalimat di papan. Subject-nya the books dan verbanya belong. Frasa on the table hanya menjelaskan lokasi."
    leo "Saat mencari rangka, abaikan sementara frasa tambahan. Jangan otomatis memilih kata benda yang paling dekat dengan verb."

    show screen day_one_speaker_portrait("reza")
    reza "Seperti memisahkan kode utama dari komentar dan konfigurasi tambahan."

    show screen day_one_speaker_portrait("leo")
    leo "Ya. Informasi tambahannya berguna, tetapi bukan pengendali struktur utama."

    show screen day_one_speaker_portrait("player")
    player "Setelah menemukan books dan belong, barulah aku memasukkan kembali informasi on the table."

    show screen day_one_speaker_portrait("leo")
    leo "Tepat."

    hide screen structure_lesson_board
    show screen structure_lesson_board("finite")
    show screen day_one_speaker_portrait("leo")
    leo "Bentuk berakhiran -ing atau bentuk to plus verb tidak dapat berdiri sendiri sebagai finite verb."
    leo "The students reviewing their notes belum menjadi klausa lengkap. Kita membutuhkan auxiliary: The students are reviewing their notes."

    show screen day_one_speaker_portrait("rina")
    rina "Berarti is, are, was, have, atau has juga perlu diperhatikan karena bisa menjadi bagian dari kelompok verba?"

    show screen day_one_speaker_portrait("leo")
    leo "Benar. Is studying dan has finished adalah kelompok verba yang lengkap."

    show screen day_one_speaker_portrait("bima")
    bima "Padahal studying hard terdengar seperti tulisan motivasi yang lengkap."

    show screen day_one_speaker_portrait("maya")
    maya "Tulisan motivasi boleh tidak lengkap. Jawaban TOEFL tidak mendapat kemewahan itu."

    show screen day_one_speaker_portrait("leo")
    leo "Kesimpulan Maya benar, meskipun penyampaiannya tidak terlalu menenangkan."

    hide screen structure_lesson_board
    show screen structure_lesson_board("agreement")
    show screen day_one_speaker_portrait("leo")
    leo "Subject dan verb harus sesuai. Dalam simple present, subject orang ketiga tunggal biasanya memakai verb berakhiran s. Subject jamak memakai bentuk dasar."
    leo "Khusus be, perhatikan pasangan is dan are, serta was dan were."

    show screen day_one_speaker_portrait("player")
    player "The student studies, tetapi the students study."

    show screen day_one_speaker_portrait("leo")
    leo "Benar. Huruf s pada noun biasanya menandakan jamak, tetapi huruf s pada present verb justru digunakan bersama subject tunggal."

    show screen day_one_speaker_portrait("reza")
    reza "Aturannya konsisten, tetapi desain simbolnya seperti sengaja dibuat untuk menjebak pengguna."

    show screen day_one_speaker_portrait("maya")
    maya "Dalam the list of grammar rules, rules memang jamak, tetapi hanya bagian dari frasa of grammar rules. Subject utamanya tetap list."

    show screen day_one_speaker_portrait("leo")
    leo "Tepat. Karena list tunggal, kita memakai appears, bukan appear."

    hide screen structure_lesson_board
    show screen structure_lesson_board("clauses")
    show screen day_one_speaker_portrait("leo")
    leo "Satu kalimat dapat memiliki lebih dari satu pasangan subject dan verb karena sebuah kalimat dapat tersusun dari beberapa clause."
    leo "Independent clause dapat menjadi kalimat lengkap. Dependent clause memiliki subject dan verb, tetapi masih bergantung pada klausa lain."

    show screen day_one_speaker_portrait("rina")
    rina "Jadi Because the room was noisy punya subject room dan verb was, tetapi masih terasa belum selesai."

    show screen day_one_speaker_portrait("leo")
    leo "Benar. Pendengar masih menunggu akibatnya. Because the room was noisy, the group moved to the library adalah kalimat lengkap."

    show screen day_one_speaker_portrait("reza")
    reza "Connector-nya seperti tanda bahwa proses berikutnya masih membutuhkan output."

    show screen day_one_speaker_portrait("bima")
    bima "Berarti dua verb tidak otomatis membuat kalimat error?"

    show screen day_one_speaker_portrait("leo")
    leo "Tidak. Yang penting, setiap verb memiliki fungsi dan clause yang jelas."

    hide screen structure_lesson_board
    show screen structure_lesson_board("relative")
    show screen day_one_speaker_portrait("leo")
    leo "Pada contoh ini, who teaches linguistics adalah relative clause yang menjelaskan professor."
    leo "Jika bagian itu kita sisihkan sementara, rangka klausa utamanya menjadi the professor explains the rule."

    show screen day_one_speaker_portrait("maya")
    maya "Jadi teaches bukan main verb. Ia milik relative clause, sedangkan explains berpasangan dengan professor."

    show screen day_one_speaker_portrait("leo")
    leo "Tepat."

    show screen day_one_speaker_portrait("player")
    player "Aku harus memeriksa batas setiap clause sebelum menentukan subject dan verb utama."

    show screen day_one_speaker_portrait("leo")
    leo "Itulah inti latihan hari ini."

    hide screen structure_lesson_board
    show screen structure_lesson_board("checklist")
    show screen day_one_speaker_portrait("leo")
    leo "Gunakan urutan di papan. Tandai batas clause, cari subject dan finite verb, abaikan modifier, lalu periksa agreement."
    leo "Sekarang kita masuk ke lima soal. Setiap jawaban benar bernilai sepuluh poin."

    hide screen structure_lesson_board
    hide screen day_one_speaker_portrait

    call screen day_two_structure_quiz(
        1,
        "___ provides students with access to thousands of digital journals.",
        "In the university library",
        "The university library",
        "The university library it"
    )
    $ structure_answer = _return
    $ structure_correct = structure_answer == "b"

    if structure_correct:
        $ day_2_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "The university library menjadi subject yang melakukan provides."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Kalimat itu sekarang memiliki satu subject dan satu finite verb yang sesuai."
    elif structure_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "In the university library?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Belum tepat. Bagian itu hanya frasa keterangan tempat, sehingga kalimatnya masih tidak memiliki subject."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "The university library it?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Pilihan itu membuat subject ganda: the university library dan it. Kita hanya membutuhkan the university library."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih B. The university library menjadi subject yang melakukan provides."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "B juga. Pilihan C membawa dua subject untuk satu posisi."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_2_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_2_structure_score]/50."

    call screen day_two_structure_quiz(
        2,
        "The students in Leo's study group ___ their notes before every practice test.",
        "reviewing",
        "to review",
        "review"
    )
    $ structure_answer = _return
    $ structure_correct = structure_answer == "c"

    if structure_correct:
        $ day_2_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya review karena subject students jamak dan kalimat membutuhkan finite verb."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. The students review adalah rangka utamanya."
    elif structure_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya reviewing?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Reviewing membutuhkan auxiliary, misalnya are reviewing. Sendirian, bentuk itu belum menjadi finite verb."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya to review?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "To review adalah infinitive dan tidak menjadi finite verb untuk klausa ini. Jawabannya review."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku memilih C. Setelah in Leo's study group disisihkan, rangkanya menjadi the students review."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "C juga. Ternyata Leo bisa dihapus sementara dari kalimat tanpa merusak grammar."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Hanya karena namaku menjadi bagian modifier dalam contoh."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Biarkan dia menikmati kemenangan kecilnya."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_2_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_2_structure_score]/50."

    call screen day_two_structure_quiz(
        3,
        "The list of difficult grammar rules ___ on the first page of the booklet.",
        "appear",
        "appearing",
        "appears"
    )
    $ structure_answer = _return
    $ structure_correct = structure_answer == "c"

    if structure_correct:
        $ day_2_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Subject utamanya list, jadi verb yang sesuai adalah appears."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Frasa of difficult grammar rules tidak mengubah subject utama yang tunggal."
    elif structure_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih appear karena melihat rules."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Itu jebakannya. Rules hanya berada di dalam modifier. Subject utamanya list, sehingga kita memakai appears."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih appearing."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Appearing tidak dapat berdiri sendiri sebagai finite verb. Kalimat ini membutuhkan appears."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih C. Subject-nya list, bukan rules."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku hampir memilih A karena rules berdiri paling dekat dengan bagian kosong."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Rules hanya kerumunan pengalih perhatian."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Karena itu cari rangka kalimat, bukan noun terdekat."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_2_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_2_structure_score]/50."

    call screen day_two_structure_quiz(
        4,
        "Although the assignment was difficult, ___.",
        "the students completed it on time",
        "completing it on time",
        "the difficult assignment"
    )
    $ structure_answer = _return
    $ structure_correct = structure_answer == "a"

    if structure_correct:
        $ day_2_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Kita membutuhkan independent clause: the students completed it on time."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Bagian itu memiliki subject students dan finite verb completed."
    elif structure_answer == "b":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Completing it on time?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Bagian itu tidak memiliki subject atau finite verb. Dependent clause di awal masih membutuhkan klausa utama yang lengkap."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "The difficult assignment?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Itu hanya noun phrase. Kita membutuhkan independent clause dengan subject dan finite verb."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aku memilih A. Bagian yang diawali although tetap membutuhkan independent clause."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "A juga. Although the boss was difficult, the party completed the quest on time."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Contohmu secara tata bahasa benar."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku akan mencatat bahwa Leo mengakui contoh gim-ku."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Catat juga bahwa itu bukan pujian penuh."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_2_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_2_structure_score]/50."

    call screen day_two_structure_quiz(
        5,
        "The professor who teaches the morning class ___ every question clearly.",
        "answer",
        "answers",
        "answering"
    )
    $ structure_answer = _return
    $ structure_correct = structure_answer == "b"

    if structure_correct:
        $ day_2_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Main subject-nya professor, jadi main verb yang sesuai adalah answers."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Who teaches the morning class hanya relative clause yang menjelaskan professor."
    elif structure_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih answer."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Main subject professor bersifat tunggal, sehingga simple present verb-nya harus answers."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih answering."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Answering membutuhkan auxiliary. Untuk melengkapi main clause ini, kita memakai answers."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Jawabanku B. Relative clause bisa dilipat sementara, lalu tersisa the professor answers every question clearly."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "B juga. Teaches milik relative clause, sedangkan answers menjadi verb klausa utama."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Jadi teaches dan explains boleh berada dalam satu kalimat karena masing-masing punya clause?"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Tepat. Dua verb bukan masalah jika struktur setiap clause jelas."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Selamat. Hari ini Bima berhasil menerima keberadaan dua verb sekaligus."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct:
        system "Jawaban benar! +10 poin. Skor akhir: [day_2_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor akhir: [day_2_structure_score]/50."

    jump day_2_after_lesson


label day_2_after_lesson:
    hide screen structure_lesson_board
    hide screen day_one_speaker_portrait
    hide normal_speaker with day_one_speaker_swap
    scene bg library study with dissolve

    if 2 not in extra_practice_days:
        call screen extra_study_quiz(
            2,
            "STRUCTURE BONUS",
            "The students ___ their notes before the tutor arrived. Pilih bentuk yang tepat.",
            "review",
            "reviewed",
            "reviewing",
            day_1_vocab_score + extra_practice_score,
            "Cari penanda waktu before the tutor arrived. Peristiwa yang selesai di masa lampau memakai pola yang konsisten."
        )
        $ extra_answer = _return
        if extra_answer == "b":
            $ extra_practice_score += 10
            system "Jawaban bonus benar! +10 poin tambahan."
        else:
            system "Jawaban bonus belum tepat. Periksa penanda waktu dan fungsi verb dalam kalimat."
        $ extra_practice_days.append(2)

    system "Skor latihan Structure Hari 2: [day_2_structure_score] dari 50 poin. Bonus kumulatif: [extra_practice_score]."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    if day_2_structure_score == 50:
        leo "Lima jawaban benar. Sempurna, [player_name]. Kamu dapat memisahkan modifier dan clause tanpa kehilangan rangka utama."
        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Perfect Structure combo! Tidak ada grammar damage yang masuk."
    elif day_2_structure_score >= 40:
        leo "Empat jawaban benar. Dasarmu sudah kuat. Tinjau satu pola yang terlewat agar kesalahan yang sama tidak berulang."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Hasil yang bagus. Cukup untuk percaya diri, belum cukup untuk menjadi ceroboh."
    elif day_2_structure_score >= 30:
        leo "Tiga jawaban benar. Kamu sudah menemukan sebagian besar rangka kalimat, tetapi agreement dan batas clause masih perlu diperiksa lebih lambat."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Kita bisa menandai subject dan verb bersama saat mengulang nanti."
    elif day_2_structure_score >= 20:
        leo "Dua jawaban benar. Singkirkan modifier lebih dahulu dan pastikan bentuk yang kamu pilih benar-benar finite verb."
        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Strukturnya belum gagal total. Parser-nya hanya perlu aturan yang lebih jelas."
    else:
        leo "Skornya masih rendah, tetapi pola kesalahannya sudah terlihat. Kita akan mengulang dari subject dan finite verb sebelum menambah pola baru."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Tidak apa-apa. Hari ini kita masih punya waktu untuk membahasnya lagi."

    hide normal_speaker with day_one_speaker_swap
    system "Setelah beristirahat sepuluh menit, Leo meminta setiap anggota membuat satu kalimat dan menunjukkan rangka utamanya."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "The notes on my desk are organized."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Benar. Notes adalah subject, are adalah verb, dan on my desk hanya modifier."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "The coffee that keeps me awake is essential."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Benar. That keeps me awake adalah relative clause. Rangka utamanya adalah the coffee is essential."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Although the boss was difficult, the party won."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Benar. Dependent clause diikuti independent clause yang lengkap."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Bima, who arrived at 07.59, considers that punctual."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Strukturnya benar."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Kenapa contoh semua orang terasa aman sampai giliran Maya?"

    show normal_speaker player at vn_center with day_one_speaker_swap
    player "The members of our study group review their notes every day."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Bagus. Main subject-nya members, jadi verb yang benar adalah review."

    hide normal_speaker with day_one_speaker_swap
    system "Pukul 11.15, papan telah dipenuhi garis bawah, lingkaran, dan tanda pemisah clause."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Cukup untuk hari ini. Ingat empat hal: temukan subject, pastikan ada finite verb, periksa agreement, dan kenali batas setiap clause."
    leo "Tugas kalian adalah menandai subject dan verb pada lima kalimat yang kukirim. Besok kita masuk ke Reading: ide pokok dan informasi rinci."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku akan memotret papan sebelum ada yang menghapusnya."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Kirim versi tanpa bayangan kepala Bima, kalau memungkinkan."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku sedang menyerap ilmu dari jarak dekat."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Kamu sedang menghalangi kamera."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Hari kedua selesai. Setidaknya sekarang kalimat panjang tidak terlihat seperti satu monster besar."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Bagus. Pecah menjadi clause, lalu cari rangkanya satu per satu."

    jump day_2_go_home


label day_2_go_home:
    play music audio.bgm_main_menu loop fadein 0.5
    hide normal_speaker with day_one_speaker_swap
    scene bg black with fade
    centered "{size=44}SORE HARI{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "[player_name] kembali ke rumah setelah sesi Structure dan meletakkan buku catatan di meja."
    player "Subject, verb, modifier, dan agreement. Ternyata mencari inti kalimat mirip membersihkan meja yang penuh barang."
    player "Leo masih akan mengirim ringkasan malam ini. Sebelum itu, aku bisa mengulang pola dari latihan tadi."

    jump day_2_evening_group_chat


label day_2_evening_group_chat:
    play music audio.bgm_main_menu loop fadein 0.5
    scene bg black with fade
    centered "{size=44}PUKUL 21.38{/size}\n{size=26}Kamar [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve

    if day_2_status == "skipped":
        system "[player_name] sedang mempelajari foto papan tulis dan lembar latihan yang dikirim teman-temannya."
        if day_1_status == "skipped":
            player "Vocabulary dan Structure sama-sama harus kukejar. Setidaknya sekarang aku sudah mulai menyusun urutannya."
        else:
            player "Catatan mereka cukup lengkap. Aku masih harus mengerjakan latihan susulannya sendiri."
    else:
        system "[player_name] baru selesai menandai ulang subject dan verb dari lima soal hari ini."

    with hpunch
    system "BZZT! Sebuah notifikasi dari grup Seven Days to TOEFL muncul."
    call screen whatsapp_day_two_summary_notification

    player "Ringkasan Structure dari Leo sudah dikirim."
    $ day_2_group_reply = renpy.call_screen("whatsapp_day_two_summary_chat")
    call screen whatsapp_day_two_summary_followup(day_2_group_reply)
    $ day_2_summary_seen = True

    if day_2_status == "in_progress":
        $ day_2_status = "completed"

    if day_2_status == "skipped":
        player "Ringkasan ini membantu, tetapi latihan susulannya tetap harus kuselesaikan."
    else:
        player "Sekarang pola Structure hari ini terasa lebih mudah diingat."

    system "[player_name] memasang alarm untuk Hari 3, mengisi daya ponsel, lalu mematikan lampu."
    jump day_2_ending


label day_2_ending:
    scene bg black with fade

    if day_2_status == "skipped":
        system "Hari kedua telah berlalu. Latihan Structure susulan masih menunggu [player_name]."
    else:
        system "Hari kedua selesai. Dasar subject, verb, agreement, dan clause telah dipelajari."

label day_2_ending_calendar:
    call screen study_calendar_day_two_to_three(
        day_one_skipped=(day_1_status == "skipped"),
        day_two_skipped=(day_2_status == "skipped"),
        day_one_makeup=day_1_makeup_pending,
        day_two_makeup=day_2_makeup_pending
    )

    $ calendar_completed_day = 2
    $ calendar_resume_label = "day_2_ending_calendar"
    $ calendar_continue_label = "day_3_afternoon"
    jump process_study_calendar


label day_3_afternoon:
    play music audio.bgm_campus loop fadein 0.5
    $ day = 3
    $ day_3_choice = ""
    $ day_3_status = "not_started"
    $ day_3_makeup_pending = False
    $ day_3_reading_score = 0
    $ day_3_summary_seen = False
    $ day_3_group_reply = ""
    $ previous_makeups = int(day_1_makeup_pending) + int(day_2_makeup_pending)

    scene bg black with fade
    centered "{size=50}HARI KETIGA{/size}\n{size=30}Reading Dasar{/size}"

    scene bg player bedroom afternoon with fade
    show mc neutral at vn_center with dissolve
    system "Senin, pukul 14.10. Setelah kelas pagi selesai lebih cepat, [player_name] sempat kembali ke rumah sebelum sesi belajar sore."
    player "Pertemuannya pukul 15.30. Aku masih punya cukup waktu untuk berganti pakaian dan memeriksa grup."

    with hpunch
    system "BZZT! Pesan baru masuk ke grup Seven Days to TOEFL."
    call screen whatsapp_day_three_confirmation_chat

    player "Ruang baca lantai dua, meja dekat rak referensi. Materi hari ini main idea dan supporting details."

    if previous_makeups == 2:
        player "Vocabulary dan Structure masih tertinggal. Aku tidak boleh menambah Reading ke daftar itu."
    elif previous_makeups == 1:
        player "Aku masih memiliki satu latihan susulan. Hari ini harus kujaga agar tidak ikut menumpuk."
    else:
        player "Dua hari pertama berhasil kulewati. Tinggal menjaga ritmenya."

    $ day_3_choice = renpy.call_screen("day_three_afternoon_choice")

    if day_3_choice == "skip":
        jump day_3_skip

    jump day_3_prepare


label day_3_skip:
    $ day_3_status = "skipped"
    $ day_3_makeup_pending = True

    player "Dosen baru saja memajukan tenggat tugas menjadi pukul lima sore. Kalau berangkat sekarang, tugas ini tidak akan selesai."
    player "Aku harus memberi kabar sebelum mereka mulai."
    system "[player_name] membuka grup, menuliskan alasannya, lalu mengirim pesan."

    call screen whatsapp_day_three_skip_chat

    scene bg black with fade
    centered "{size=44}PUKUL 17.12{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "Tugas yang dikirim pukul 16.56 sudah diterima. Foto passage dan lembar latihan kini menunggu di grup."

    if previous_makeups == 2:
        player "Sekarang tiga sesi tertinggal. Besok aku harus datang lebih awal dan benar-benar mengikuti rencana Leo."
    elif previous_makeups == 1:
        player "Dua latihan susulan harus segera kuselesaikan sebelum materi berikutnya datang."
    else:
        player "Aku melewatkan sesi hari ini, tetapi materi Reading-nya tetap harus kupelajari."

    jump day_3_evening_group_chat


label day_3_prepare:
    play music audio.bgm_study loop fadein 0.5
    $ day_3_status = "in_progress"
    $ day_3_makeup_pending = False

    if previous_makeups == 2:
        player "Dua sesi sudah terlewat. Hari ini aku harus hadir."
    elif previous_makeups == 1:
        player "Satu latihan susulan sudah cukup. Aku tidak akan menambahnya."
    else:
        player "Tiga hari berturut-turut. Ritme ini harus dipertahankan."

    if day_2_status == "skipped":
        system "[player_name] berganti pakaian, lalu memasukkan catatan Structure susulan, buku catatan, dan highlighter ke dalam tas."
    else:
        system "[player_name] berganti pakaian, lalu memasukkan tugas Structure, buku catatan, dan highlighter ke dalam tas."
    player "Semua lengkap. Saatnya mencari main idea tanpa tersesat ke kantin."

    scene bg black with fade
    centered "{size=44}PUKUL 15.20{/size}\n{size=26}Perpustakaan Kampus • Lantai Dua{/size}"

    scene bg library study with fade
    system "[player_name] tiba di meja dekat rak referensi. Lima kursi sudah terisi, sedangkan satu kursi kosong telah disiapkan untuknya."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku menyimpan enam kursi dan hampir diminta mengisi formulir reservasi."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Dedikasimu sudah mencapai tingkat administratif."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku membawa passage, highlighter, dan kopi yang tidak boleh berada dekat passage."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Bima sudah mencoba menebak main idea hanya dari judul."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Itu namanya strategi speedrun."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Judul adalah petunjuk, bukan jaminan jawaban."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Berarti hari ini kita membaca dulu sebelum melakukan speedrun."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Sistem yang sangat membatasi kreativitas."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    if day_2_status == "skipped":
        leo "Tugas Structure-mu masih berupa latihan susulan. Setelah sesi Reading, kita atur bagian yang harus kamu kerjakan lebih dahulu."
    else:
        system "[player_name] menyerahkan lembar tugas Structure kepada Leo."
        leo "Tugas Structure sudah kukumpulkan. Saat istirahat nanti, aku akan menandai pola yang masih perlu kalian perbaiki."

    if previous_makeups == 2:
        leo "Bagus kamu datang. Setelah sesi ini, kita susun urutan latihan susulan Vocabulary dan Structure."
    elif previous_makeups == 1:
        leo "Setelah Reading selesai, jangan lupa materi yang masih tertinggal. Kita atur agar latihannya tidak bertabrakan."
    else:
        leo "Kehadiranmu konsisten. Pertahankan sampai simulasi akhir."

    hide normal_speaker with day_one_speaker_swap
    system "Pukul 15.30 tepat, Leo membagikan satu passage kepada setiap anggota dan berdiri di dekat papan."

    jump day_3_reading_lesson


label day_3_reading_lesson:
    play music audio.bgm_study loop fadein 0.5
    scene bg library study with dissolve

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Hari ketiga kita masuk ke Reading. Target kita bukan menerjemahkan setiap kata, tetapi memahami struktur bacaan dan menemukan bukti untuk setiap jawaban."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Jadi kalau ada tiga atau empat kata yang tidak kukenal, aku tidak perlu berhenti membaca?"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Tidak. Selama kamu masih memahami hubungan antargagasan, lanjutkan. Kembali ke kata itu hanya jika pertanyaannya memang membutuhkan."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Berarti Reading bukan misi membuka seratus persen isi kamus."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Kemajuan. Sekarang tinggal memastikan kamu benar-benar membaca teksnya."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Cari informasi yang diminta, lacak sumbernya, lalu verifikasi jawabannya."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Tepat. Setiap jawaban harus kembali pada bukti di passage."

    hide normal_speaker with day_one_speaker_swap
    show screen reading_lesson_board("overview")
    show screen day_one_speaker_portrait("leo")
    leo "Mulailah dengan tujuan yang jelas. Kenali jenis pertanyaan, cari bagian passage yang relevan, lalu tuntut bukti untuk jawabanmu."
    leo "Perhatikan juga penanda seperti however, although, dan for these reasons. Kata-kata itu menunjukkan hubungan atau perubahan arah gagasan."
    show screen day_one_speaker_portrait("reza")
    reza "Seperti penanda alur. However memberi tahu bahwa arah pembahasan akan berubah."
    show screen day_one_speaker_portrait("leo")
    leo "Benar. Struktur paragraf sering lebih membantu daripada menerjemahkan kata satu per satu."

    hide screen reading_lesson_board
    show screen reading_lesson_board("main_idea")
    show screen day_one_speaker_portrait("leo")
    leo "Topic menjawab apa yang dibahas. Main idea menggabungkan topic dengan pesan utama penulis tentang topic itu."
    show screen day_one_speaker_portrait("rina")
    rina "Kalau passage menjelaskan sebuah masalah lalu menawarkan solusi, main idea harus mencakup kedua bagian itu?"
    show screen day_one_speaker_portrait("leo")
    leo "Tepat. Jawaban yang hanya menyebut satu contoh terlalu sempit, sedangkan klaim yang melampaui passage terlalu luas."
    show screen day_one_speaker_portrait("maya")
    maya "Pilihan dengan only, always, atau completely juga patut dicurigai jika teks tidak sekuat itu."
    show screen day_one_speaker_portrait("leo")
    leo "Benar. Kata ekstrem memerlukan bukti yang sama kuatnya."

    hide screen reading_lesson_board
    show screen reading_lesson_board("details")
    show screen day_one_speaker_portrait("leo")
    leo "Untuk pertanyaan detail, ambil keyword atau sinonim dari pertanyaan. Setelah menemukannya, baca kalimat itu bersama konteks di sekitarnya."
    show screen day_one_speaker_portrait("player")
    player "Lalu aku memilih jawaban yang menyampaikan informasi sama, meskipun susunan katanya berbeda."
    show screen day_one_speaker_portrait("leo")
    leo "Benar. TOEFL sering menguji parafrasa, bukan salinan kalimat yang sama persis."
    show screen day_one_speaker_portrait("bima")
    bima "Jadi jawabannya memakai skin berbeda, tetapi statistiknya sama."
    show screen day_one_speaker_portrait("maya")
    maya "Perumpamaan itu masih bisa ditoleransi."

    hide screen reading_lesson_board
    show screen reading_lesson_board("reference_vocab")
    show screen day_one_speaker_portrait("leo")
    leo "Pada reference question, jangan otomatis memilih noun terdekat. Antecedent harus cocok secara jumlah dan makna."
    show screen day_one_speaker_portrait("reza")
    reza "Ganti pronoun dengan calon jawabannya, lalu jalankan ulang kalimat."
    show screen day_one_speaker_portrait("leo")
    leo "Cara itu efektif. Untuk vocabulary, gunakan strategi Hari 1: ganti kata target dengan pilihan, lalu periksa apakah konteksnya tetap masuk akal."
    show screen day_one_speaker_portrait("rina")
    rina "Jadi pilihan yang terdengar familiar tetap salah kalau merusak hubungan antarkalimat."
    show screen day_one_speaker_portrait("leo")
    leo "Tepat."

    hide screen reading_lesson_board
    show screen reading_lesson_board("inference")
    show screen day_one_speaker_portrait("leo")
    leo "Inference bukan tebakan bebas. Jawabannya mungkin tidak dinyatakan dengan kata yang sama, tetapi harus menjadi kesimpulan paling kuat dari bukti."
    show screen day_one_speaker_portrait("bima")
    bima "Jadi inference bukan izin membuat fanfiction dari passage."
    show screen day_one_speaker_portrait("maya")
    maya "Itu definisi paling akurat yang kamu hasilkan minggu ini."
    show screen day_one_speaker_portrait("leo")
    leo "Gunakan kesimpulan yang hati-hati. Jangan menambahkan asumsi pribadi atau kepastian yang tidak diberikan teks."

    hide screen reading_lesson_board
    show screen reading_lesson_board("checklist")
    show screen day_one_speaker_portrait("leo")
    leo "Sebelum memilih, pastikan kamu tahu jenis pertanyaannya dan dapat menunjukkan kalimat yang menjadi bukti."
    leo "Sekarang baca passage Urban Trees. Passage tetap tersedia selama lima soal. Setiap jawaban benar bernilai sepuluh poin."

    hide screen reading_lesson_board
    hide screen day_one_speaker_portrait

    call screen day_three_reading_quiz(
        1,
        "URBAN TREES",
        day_three_reading_passage,
        "What is the main idea of the passage?",
        "Cities should use trees as their only method of controlling pollution.",
        "Urban trees provide benefits, but successful programs require planning and continued care.",
        "Most tree species can grow successfully in any urban region."
    )
    $ reading_answer = _return
    $ reading_correct = reading_answer == "b"

    if reading_correct:
        $ day_3_reading_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya B. Passage membahas manfaat pohon sekaligus perencanaan dan perawatan yang dibutuhkan."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Pilihan itu mencakup seluruh arah passage."
    elif reading_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A karena passage membahas polusi."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "A terlalu sempit dan terlalu ekstrem. Teks justru mengatakan pohon tidak dapat menggantikan usaha mengurangi polusi dari sumbernya."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C karena passage membahas banyak jenis pohon."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "C tidak didukung teks. Passage hanya mengatakan kecocokan dapat berbeda antarwilayah, bukan bahwa sebagian besar spesies cocok di semua wilayah."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih B. Setelah however, passage beralih dari manfaat ke kebutuhan perencanaan dan perawatan."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "A memakai only, sedangkan C membuat generalisasi tentang sebagian besar spesies. Keduanya lebih kuat daripada bukti teks."

    hide normal_speaker with day_one_speaker_swap
    if reading_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_3_reading_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_3_reading_score]/50."

    call screen day_three_reading_quiz(
        2,
        "URBAN TREES",
        day_three_reading_passage,
        "According to the passage, how do trees help city streets during hot weather?",
        "They cause more rain to fall near roads.",
        "They remove all airborne particles from the city.",
        "Their shade lowers surface temperatures."
    )
    $ reading_answer = _return
    $ reading_correct = reading_answer == "c"

    if reading_correct:
        $ day_3_reading_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya C. Shade dari pohon menurunkan suhu permukaan jalan dan trotoar."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Itu parafrasa langsung dari kalimat kedua."
    elif reading_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, pohon membuat lebih banyak hujan turun."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Informasi itu tidak pernah disebutkan. Kembali ke kalimat yang membahas hot weather."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B karena daun menangkap partikel udara."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Teks hanya mengatakan some particles, bukan all. Pertanyaannya juga khusus menanyakan hot weather."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Jawabanku C. Kalimat kedua langsung menghubungkan shade dengan lower surface temperatures."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Berarti shade memberi area buff terhadap suhu jalan."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Istilahnya teduh, tetapi inti jawabanmu benar."

    hide normal_speaker with day_one_speaker_swap
    if reading_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_3_reading_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_3_reading_score]/50."

    call screen day_three_reading_quiz(
        3,
        "URBAN TREES",
        day_three_reading_passage,
        "The word 'they' in 'they select suitable species' refers to...",
        "successful tree-planting programs",
        "suitable species",
        "young trees"
    )
    $ reading_answer = _return
    $ reading_correct = reading_answer == "a"

    if reading_correct:
        $ day_3_reading_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "They merujuk pada successful tree-planting programs. Program itulah yang memilih spesies dan menyediakan perawatan."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Antecedent-nya cocok secara plural dan logis melakukan kedua tindakan itu."
    elif reading_answer == "b":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "They merujuk pada suitable species?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Tidak. Suitable species muncul setelah pronoun, dan spesies tidak memilih dirinya sendiri serta menyediakan perawatan."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "They merujuk pada young trees?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Jumlahnya cocok, tetapi maknanya tidak. Young trees tidak menjalankan program pemilihan spesies."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aku memilih A. Setelah diganti, kalimatnya tetap logis: the programs select suitable species and provide care."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku sempat melihat trees karena sama-sama plural."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Jumlah saja belum cukup. Maknanya juga harus cocok."

    hide normal_speaker with day_one_speaker_swap
    if reading_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_3_reading_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_3_reading_score]/50."

    call screen day_three_reading_quiz(
        4,
        "URBAN TREES",
        day_three_reading_passage,
        "The word 'struggle' in the passage is closest in meaning to...",
        "grow rapidly",
        "have difficulty",
        "become widely available"
    )
    $ reading_answer = _return
    $ reading_correct = reading_answer == "b"

    if reading_correct:
        $ day_3_reading_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Struggle paling dekat artinya have difficulty."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Grows well di satu wilayah dikontraskan dengan struggle di wilayah lain."
    elif reading_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Struggle berarti grow rapidly?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Itu berlawanan dengan konteks. Perbedaan hujan, tanah, dan suhu membuat spesies tersebut mengalami kesulitan."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Struggle berarti become widely available?"
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Tidak. Passage membahas kemampuan spesies untuk tumbuh, bukan ketersediaannya."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih B. Grows well dikontraskan dengan struggle."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Proses pertumbuhannya tidak berjalan mulus, bukan tiba-tiba mendapat peningkatan kecepatan."

    hide normal_speaker with day_one_speaker_swap
    if reading_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_3_reading_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_3_reading_score]/50."

    call screen day_three_reading_quiz(
        5,
        "URBAN TREES",
        day_three_reading_passage,
        "What can be inferred about a program that does not care for trees after planting them?",
        "It will not need to select suitable species.",
        "It will completely eliminate pollution near city streets.",
        "It may fail to provide communities with long-term tree benefits."
    )
    $ reading_answer = _return
    $ reading_correct = reading_answer == "c"

    if reading_correct:
        $ day_3_reading_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya C. Tanpa perawatan lanjutan, program itu mungkin gagal memberi manfaat pohon dalam jangka panjang."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Kata may membuat kesimpulannya hati-hati dan tetap didukung hubungan antara long-term care dan manfaat jangka panjang."
    elif reading_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, program itu tidak perlu memilih spesies yang sesuai."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Justru sebaliknya. Passage menyebut pemilihan suitable species sebagai bagian dari program yang berhasil."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B, program itu akan menghilangkan polusi sepenuhnya."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Teks menolak klaim itu. Pohon tidak dapat menggantikan usaha mengurangi polusi pada sumbernya."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku memilih C. Kalau program hanya menanam lalu meninggalkan pohonnya, quest-nya berhenti setelah tutorial."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aneh, tetapi kesimpulannya benar."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "C adalah inference paling aman. Bukti mendukungnya tanpa menjanjikan hasil mutlak."

    hide normal_speaker with day_one_speaker_swap
    if reading_correct:
        system "Jawaban benar! +10 poin. Skor akhir: [day_3_reading_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor akhir: [day_3_reading_score]/50."

    jump day_3_after_lesson


label day_3_after_lesson:
    hide screen reading_lesson_board
    hide screen day_one_speaker_portrait
    hide normal_speaker with day_one_speaker_swap
    scene bg library study with dissolve

    if 3 not in extra_practice_days:
        call screen extra_study_quiz(
            3,
            "READING BONUS",
            "Passage: The campus added shaded benches near the library. Students now spend more time reading outdoors.\n\nWhat is the main idea?",
            "The benches discourage students from reading.",
            "Shaded benches encourage students to read outside.",
            "The library has been closed permanently.",
            day_1_vocab_score + day_2_structure_score + extra_practice_score,
            "Main idea harus merangkum hubungan fasilitas baru dan perubahan perilaku siswa, bukan detail yang tidak disebutkan."
        )
        $ extra_answer = _return
        if extra_answer == "b":
            $ extra_practice_score += 10
            system "Jawaban bonus benar! +10 poin tambahan."
        else:
            system "Jawaban bonus belum tepat. Cari gagasan yang mencakup sebab dan dampak."
        $ extra_practice_days.append(3)

    system "Skor latihan Reading Hari 3: [day_3_reading_score] dari 50 poin. Bonus kumulatif: [extra_practice_score]."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    if day_3_reading_score == 50:
        leo "Lima jawaban benar. Sempurna, [player_name]. Kamu membedakan informasi langsung, reference, dan inference dengan sangat teliti."
        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Perfect Reading run! Semua bukti berhasil ditemukan."
    elif day_3_reading_score >= 40:
        leo "Empat jawaban benar. Strategimu sudah kuat. Periksa satu jawaban yang belum memiliki bukti paling tepat."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Bagus. Pertahankan ketelitian itu sebelum mulai merasa bisa membaca pikiran penulis."
    elif day_3_reading_score >= 30:
        leo "Tiga jawaban benar. Kamu sudah memahami isi umum, tetapi masih perlu membedakan bukti langsung dan inference."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Kita bisa menandai kalimat bukti untuk setiap jawaban saat mengulang."
    elif day_3_reading_score >= 20:
        leo "Dua jawaban benar. Jangan memilih dari ingatan. Kembali ke passage dan cocokkan setiap pilihan dengan kalimat bukti."
        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Datanya tersedia. Kita hanya perlu memperbaiki cara pencariannya."
    else:
        leo "Skornya masih rendah, tetapi sekarang jenis kesalahannya terlihat. Mulailah dari detail dan reference sebelum melatih inference."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Tidak apa-apa. Passage-nya bisa kita bedah lagi satu pertanyaan demi satu."

    hide normal_speaker with day_one_speaker_swap
    system "Setelah istirahat singkat, Leo meminta setiap anggota menyebutkan satu aturan yang akan mereka gunakan pada passage berikutnya."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Untuk detail, aku akan mencari keyword atau sinonimnya lalu membaca kalimat di sekitarnya."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Untuk reference, aku akan mengganti pronoun dengan calon antecedent dan memeriksa apakah kalimatnya masih logis."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Untuk main idea, aku akan memilih jawaban yang mencakup seluruh arah passage, bukan detail yang kebetulan terdengar penting."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Untuk inference, aku tidak akan menulis fanfiction dari passage."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Versi resminya: jangan menambahkan asumsi yang tidak didukung teks."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Dan untuk semua jenis soal, aku harus bisa menunjukkan kalimat yang mendukung jawabanku."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Bagus. Besok kita masuk ke Listening: percakapan pendek dan informasi penting."

    hide normal_speaker with day_one_speaker_swap
    system "Pukul 17.25, Leo membagikan satu passage pendek sebagai tugas. Setiap anggota harus menulis main idea dan memilih dua supporting details."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Main idea sesi hari ini adalah kelompok kita pantas mendapat makanan."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Tidak ada supporting detail yang mendukung kesimpulan itu."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Berarti jawaban Bima harus dieliminasi karena tidak didukung passage."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Tepat. Ringkasan Reading akan kukirim setelah makan malam."

    jump day_3_go_home


label day_3_go_home:
    play music audio.bgm_main_menu loop fadein 0.5
    hide normal_speaker with day_one_speaker_swap
    scene bg black with fade
    centered "{size=44}PUKUL 18.20{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "[player_name] kembali ke rumah dan meletakkan passage yang penuh tanda warna di atas meja."
    player "Topic menunjukkan apa yang dibahas. Main idea menjelaskan inti yang disampaikan tentang topic itu."
    player "Supporting details harus menjadi bukti, bukan sekadar kalimat yang kebetulan terlihat penting."

    if previous_makeups:
        player "Materi Reading hari ini sudah aman. Sekarang aku tetap harus mengejar materi sebelumnya."

    jump day_3_evening_group_chat


label day_3_evening_group_chat:
    play music audio.bgm_main_menu loop fadein 0.5
    scene bg black with fade
    centered "{size=44}PUKUL 21.26{/size}\n{size=26}Kamar [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve

    if day_3_status == "skipped":
        system "[player_name] baru selesai membaca foto passage dan catatan yang dikirim kelompok."
    else:
        system "[player_name] baru selesai menandai ulang bukti untuk lima soal Reading hari ini."

    with hpunch
    system "BZZT! Sebuah notifikasi dari grup Seven Days to TOEFL muncul."
    call screen whatsapp_day_three_summary_notification

    player "Ringkasan Reading dari Leo sudah masuk."
    $ day_3_group_reply = renpy.call_screen("whatsapp_day_three_summary_chat")
    call screen whatsapp_day_three_summary_followup(day_3_group_reply)
    $ day_3_summary_seen = True

    if day_3_status == "in_progress":
        $ day_3_status = "completed"

    if day_3_status == "skipped":
        player "Ringkasannya sudah jelas. Sekarang latihan Reading susulannya harus benar-benar kukerjakan."
    else:
        player "Strategi Reading hari ini terasa lebih teratur setelah diringkas seperti ini."

    system "[player_name] memasang pengingat sesi Listening, mengisi daya ponsel, lalu beristirahat."
    jump day_3_ending


label day_3_ending:
    scene bg black with fade

    if day_3_status == "skipped":
        system "Hari ketiga telah berlalu. Latihan Reading susulan masih menunggu [player_name]."
    else:
        system "Hari ketiga selesai. Main idea, supporting details, reference, vocabulary, dan inference telah dipelajari."

label day_3_ending_calendar:
    call screen study_calendar_day_three_to_four(
        day_one_skipped=(day_1_status == "skipped"),
        day_two_skipped=(day_2_status == "skipped"),
        day_three_skipped=(day_3_status == "skipped"),
        day_one_makeup=day_1_makeup_pending,
        day_two_makeup=day_2_makeup_pending,
        day_three_makeup=day_3_makeup_pending
    )

    $ calendar_completed_day = 3
    $ calendar_resume_label = "day_3_ending_calendar"
    $ calendar_continue_label = "day_4_afternoon"
    jump process_study_calendar


label day_4_afternoon:
    play music audio.bgm_campus loop fadein 0.5
    $ day = 4
    $ day_4_choice = ""
    $ day_4_status = "not_started"
    $ day_4_makeup_pending = False
    $ day_4_listening_score = 0
    $ day_4_summary_seen = False
    $ day_4_group_reply = ""
    $ day_4_backlog_plan_made = False
    $ prior_backlog_day4 = int(day_1_makeup_pending) + int(day_2_makeup_pending) + int(day_3_makeup_pending)

    scene bg black with fade
    centered "{size=50}HARI KEEMPAT{/size}\n{size=30}Listening: Short Conversations{/size}"

    scene bg player bedroom afternoon with fade
    show mc neutral at vn_center with dissolve
    system "Selasa, pukul 14.00. Setelah makan siang, [player_name] kembali ke rumah untuk mengambil earphone dan catatan."
    player "Sesi Listening dimulai pukul 15.30 di Laboratorium Bahasa. Masih ada waktu untuk memeriksa perlengkapan."

    with hpunch
    system "BZZT! Grup Seven Days to TOEFL kembali ramai."
    call screen whatsapp_day_four_confirmation_chat

    if prior_backlog_day4 == 3:
        player "Tiga materi masih tertunda dan aku sudah berjanji bertemu Leo pukul 15.00."
    elif prior_backlog_day4 == 2:
        player "Dua latihan susulan masih menunggu. Listening tidak boleh ikut menumpuk."
    elif prior_backlog_day4 == 1:
        player "Masih ada satu materi tertunda. Hari ini aku harus menjaga ritme."
    else:
        player "Tiga hari pertama sudah selesai. Aku ingin mempertahankan catatan kehadiran ini."

    $ day_4_choice = renpy.call_screen("day_four_afternoon_choice")

    if day_4_choice == "skip":
        jump day_4_skip

    jump day_4_prepare


label day_4_skip:
    $ day_4_status = "skipped"
    $ day_4_makeup_pending = True
    $ day_4_total_backlog = prior_backlog_day4 + 1

    player "Sakit kepalaku semakin berat sejak siang. Memaksakan diri mendengarkan audio hanya akan membuatku kehilangan fokus."
    player "Aku harus memberi kabar sekarang, sebelum mereka mulai."
    system "[player_name] membuka grup dan mengirim pesan izin."

    call screen whatsapp_day_four_skip_chat

    scene bg black with fade
    centered "{size=44}PUKUL 18.05{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "Setelah beristirahat, sakit kepala [player_name] mulai berkurang. Rekaman, lembar soal, dan foto catatan sudah masuk ke grup."

    if day_4_total_backlog >= 3:
        player "Besok aku harus datang pukul 14.45 dan menyusun cara mengejar semua materi ini bersama Leo."
    elif day_4_total_backlog == 2:
        player "Dua sesi tertunda masih bisa dikejar kalau aku mulai mengaturnya malam ini."
    else:
        player "Listening hari ini terlewat, tetapi rekamannya tetap harus kudengarkan."

    jump day_4_evening_group_chat


label day_4_prepare:
    play music audio.bgm_exam loop fadein 0.5
    $ day_4_status = "in_progress"
    $ day_4_makeup_pending = False

    if prior_backlog_day4 == 3:
        player "Aku sudah melewatkan tiga materi. Pertemuan lebih awal dengan Leo tidak boleh ikut terlewat."
    elif prior_backlog_day4:
        player "Latihan susulan masih ada, tetapi menambah satu lagi bukan solusi. Aku harus berangkat."
    else:
        player "Earphone siap, catatan siap. Semoga telingaku juga siap."

    if day_3_status == "skipped":
        system "[player_name] memasukkan lembar Reading susulan, earphone, dan buku catatan ke dalam tas."
    else:
        system "[player_name] memasukkan tugas Reading, earphone, dan buku catatan ke dalam tas."

    if prior_backlog_day4 == 3:
        scene bg black with fade
        centered "{size=44}PUKUL 15.00{/size}\n{size=26}Laboratorium Bahasa • Gedung B{/size}"

        scene bg language laboratory with fade
        system "Leo sudah menunggu di meja depan sebelum anggota lain datang."

        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Kita tidak akan mengejar tiga materi sekaligus. Kita susun urutannya."
        leo "Malam ini ulang Vocabulary selama dua puluh menit. Besok pukul 14.45 kita bahas Structure dasar sebelum materi lanjutan."
        leo "Setelah Hari 5, kita sisihkan waktu untuk passage Reading."

        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Baik. Satu per satu, tetapi tidak ada yang dibiarkan tertinggal lagi."
        $ day_4_backlog_plan_made = True
    else:
        scene bg black with fade
        centered "{size=44}PUKUL 15.20{/size}\n{size=26}Laboratorium Bahasa • Gedung B{/size}"

        scene bg language laboratory with fade
        system "[player_name] tiba sepuluh menit sebelum sesi dimulai. Beberapa komputer dan headset sudah menyala."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Headset nomor empat hanya mengeluarkan suara di kiri. Aku sudah menandainya."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku memindahkan adaptor cadangan ke meja tengah. Siapa pun boleh memakainya."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku baru sadar tanda L dan R bukan tingkat kesulitan."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "L itu left, bukan low difficulty. Earphone-mu juga terpasang terbalik."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Lima menit di laboratorium dan kita sudah mendapat materi tambahan."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Duduk dan periksa volume. Jangan langsung menaikkannya sampai maksimal. Kita mulai tepat pukul 15.30."

    hide normal_speaker with day_one_speaker_swap
    system "Setiap anggota mencoba headsetnya. Indikator audio di layar bergerak, lalu ruangan menjadi tenang."

    jump day_4_listening_lesson


label day_4_listening_lesson:
    stop music fadeout 0.5
    scene bg language laboratory with dissolve

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Hari keempat kita berlatih Listening. Kalian tidak perlu mengingat setiap kata. Tangkap situasi, informasi penting, dan alasan pembicara mengatakan sesuatu."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Kalau satu kalimat terlewat karena pembicaranya terlalu cepat?"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Jangan berhenti memikirkan kalimat yang hilang. Ikuti percakapan berikutnya dan perhatikan respons terakhir."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Jadi proses informasi yang berhasil ditangkap, bukan mengulang paket yang sudah hilang."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Apakah transkrip termasuk fitur subtitle?"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Transkrip baru dibuka setelah kalian menjawab. Setiap audio boleh diputar ulang satu kali."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Hari yang berat bagi pemain yang selalu menyalakan subtitle sebelum gim dimulai."

    hide normal_speaker with day_one_speaker_swap
    show screen listening_lesson_board("overview")
    show screen day_one_speaker_portrait("leo")
    leo "Pada putaran pertama, cari situasinya. Siapa yang berbicara, apa yang mereka bahas, dan apakah terjadi masalah atau perubahan."
    show screen day_one_speaker_portrait("player")
    player "Aku tidak perlu menulis seluruh kalimat. Cukup kata penting dan hubungan antargagasan."
    show screen day_one_speaker_portrait("leo")
    leo "Benar. Catatan seperti room full lalu meet upstairs sudah lebih berguna daripada mencoba menyalin semuanya."

    hide screen listening_lesson_board
    show screen listening_lesson_board("main_idea")
    show screen day_one_speaker_portrait("leo")
    leo "Main idea merangkum apa yang sedang diselesaikan atau diputuskan oleh kedua pembicara."
    show screen day_one_speaker_portrait("maya")
    maya "Satu kata yang sering terdengar belum tentu menjadi topik utama."
    show screen day_one_speaker_portrait("bima")
    bima "Jadi kalau mereka menyebut kopi sekali, main idea-nya belum tentu kopi."
    show screen day_one_speaker_portrait("reza")
    reza "Kecuali seluruh masalah selesai setelah kopinya datang."

    hide screen listening_lesson_board
    show screen listening_lesson_board("detail")
    show screen day_one_speaker_portrait("leo")
    leo "Detail question meminta informasi tertentu. Perhatikan jika pembicara mengoreksi dugaan sebelumnya."
    show screen day_one_speaker_portrait("rina")
    rina "Kalau seseorang berkata I thought it was on the desk, lalu temannya menunjukkan lokasi lain, jawaban akhirnya lokasi yang dikonfirmasi?"
    show screen day_one_speaker_portrait("leo")
    leo "Tepat. Jangan berhenti pada informasi pertama."

    hide screen listening_lesson_board
    show screen listening_lesson_board("intent_suggestion")
    show screen day_one_speaker_portrait("leo")
    leo "Intent question menanyakan tujuan ucapan, bukan hanya arti literalnya. Sebuah deadline dapat disebutkan untuk menjelaskan mengapa seseorang tidak bisa hadir."
    show screen day_one_speaker_portrait("maya")
    maya "Konteks menentukan apakah seseorang sedang menjelaskan, menolak, meminta bantuan, atau menyarankan sesuatu."
    show screen day_one_speaker_portrait("leo")
    leo "Untuk suggestion, kenali ungkapan seperti why don't you, you could, atau maybe we should."

    hide screen listening_lesson_board
    show screen listening_lesson_board("inference")
    show screen day_one_speaker_portrait("leo")
    leo "Inference tidak selalu diucapkan langsung. Namun, kesimpulannya harus mengikuti bukti dengan wajar dan membutuhkan asumsi sesedikit mungkin."
    show screen day_one_speaker_portrait("bima")
    bima "Dengan kata lain, jangan membuat cutscene tambahan di kepala."
    show screen day_one_speaker_portrait("maya")
    maya "Versi formalnya benar."
    show screen day_one_speaker_portrait("leo")
    leo "Perhatikan kata yang menunjukkan perasaan atau hasil, seperti relieved, unfortunately, only, dan finally."

    hide screen listening_lesson_board
    show screen listening_lesson_board("checklist")
    show screen day_one_speaker_portrait("leo")
    leo "Sebelum memilih, tentukan jenis pertanyaannya, cari perubahan informasi, lalu periksa fungsi respons terakhir."
    leo "Kalian akan mengerjakan lima soal. Setiap jawaban benar bernilai sepuluh poin. Kenakan headset dan tunggu sampai audio selesai."

    hide screen listening_lesson_board
    hide screen day_one_speaker_portrait

    jump day_4_listening_question_1


label day_4_listening_question_1:
    call screen day_four_listening_quiz(
        1,
        audio.day4_q1,
        "What are the speakers mainly discussing?",
        "Why the library closes at five",
        "Where their group should meet",
        "How to reserve a room online"
    )
    $ listening_answer = _return
    stop listening
    $ listening_correct = listening_answer == "b"
    if listening_correct:
        $ day_4_listening_score += 10

    call screen day_four_listening_transcript(
        1,
        "WOMAN: Did you reserve the study room for this afternoon?\n\nMAN: I tried, but every room is booked until five.\n\nWOMAN: Then let's meet at the tables near the second-floor windows. They're usually quiet.\n\nMAN: Good idea. I'll tell the rest of the group.",
        "Bukti: ruang belajar penuh, lalu mereka memutuskan lokasi pertemuan pengganti."
    )

    if listening_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya B. Mereka sedang menentukan tempat kelompok akan bertemu."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Ruang belajar penuh, lalu mereka memilih meja dekat jendela lantai dua."
    elif listening_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A karena mendengar until five."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Pukul lima hanya detail tentang ketersediaan ruangan. Mereka tidak membahas waktu perpustakaan tutup."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C karena pria itu mencoba melakukan reservasi."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Proses reservasinya tidak dijelaskan. Fokus percakapannya adalah lokasi pertemuan."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih B. Keputusan akhirnya adalah bertemu di meja lantai dua."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Ruang utama penuh, jadi party pindah ke alternate meeting point."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Yang secara akademis disebut lokasi pengganti."
    hide normal_speaker with day_one_speaker_swap
    if listening_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_4_listening_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_4_listening_score]/50."

    jump day_4_listening_question_2


label day_4_listening_question_2:
    call screen day_four_listening_quiz(
        2,
        audio.day4_q2,
        "Where is the man's flash drive?",
        "Beside the computer",
        "Inside a desk drawer",
        "In the pocket of his blue folder"
    )
    $ listening_answer = _return
    stop listening
    $ listening_correct = listening_answer == "c"
    if listening_correct:
        $ day_4_listening_score += 10

    call screen day_four_listening_transcript(
        2,
        "MAN: I can't find my flash drive. I thought I left it beside the computer.\n\nWOMAN: You put it in the small pocket of your blue folder after the presentation. I saw you zip it closed.\n\nMAN: You're right. It's still there.",
        "Bukti: lokasi di folder biru disebutkan lalu dikonfirmasi dengan You're right."
    )

    if listening_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya C. Flash drive-nya berada di saku kecil folder biru."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Wanita menyebut lokasinya dan pria mengonfirmasinya."
    elif listening_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, di samping komputer."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Beside the computer hanya dugaan awal. Dengarkan koreksi setelahnya."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B, di dalam laci meja."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Desk drawer tidak pernah disebutkan dalam percakapan."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku memilih C. Kalimat You're right memastikan informasi terakhir adalah jawaban."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Item-nya tersimpan di inventory folder, bukan hilang."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Masalahnya bukan inventory. Pemiliknya lupa lokasi penyimpanan."
    hide normal_speaker with day_one_speaker_swap
    if listening_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_4_listening_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_4_listening_score]/50."

    jump day_4_listening_question_3


label day_4_listening_question_3:
    call screen day_four_listening_quiz(
        3,
        audio.day4_q3,
        "Why does the man mention his statistics report?",
        "To explain why he cannot attend the review session",
        "To ask the woman for help with the report",
        "To suggest changing the topic of the session"
    )
    $ listening_answer = _return
    stop listening
    $ listening_correct = listening_answer == "a"
    if listening_correct:
        $ day_4_listening_score += 10

    call screen day_four_listening_transcript(
        3,
        "WOMAN: Are you coming to the review session tonight?\n\nMAN: I have a statistics report due first thing tomorrow morning.\n\nWOMAN: So I should tell the tutor you can't make it?\n\nMAN: Unfortunately, yes.",
        "Bukti: deadline laporan menjelaskan mengapa pria tidak dapat menghadiri sesi review."
    )

    if listening_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya A. Dia menyebut laporan untuk menjelaskan mengapa tidak bisa datang."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Respons wanita dan kata unfortunately mengonfirmasi maksud itu."
    elif listening_answer == "b":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B. Mungkin dia ingin dibantu mengerjakan laporan."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Tidak ada permintaan bantuan. Laporan itu hanya menjelaskan konflik waktunya."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C, mengubah topik sesi menjadi statistik."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Dia tidak mengusulkan perubahan topik. Statistics report adalah alasan ketidakhadirannya."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aku memilih A. Laporan itu berfungsi sebagai alasan, bukan permintaan."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Dan unfortunately menunjukkan dia sebenarnya tidak senang harus melewatkan sesi."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Deadline side quest mengunci akses ke main session."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Perumpamaanmu tepat, meskipun prioritas quest-nya dapat diperdebatkan."
    hide normal_speaker with day_one_speaker_swap
    if listening_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_4_listening_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_4_listening_score]/50."

    jump day_4_listening_question_4


label day_4_listening_question_4:
    call screen day_four_listening_quiz(
        4,
        audio.day4_q4,
        "What does the woman suggest the man do?",
        "Buy paper for the library printer",
        "Use the printer in the student center",
        "Submit the form the following day"
    )
    $ listening_answer = _return
    stop listening
    $ listening_correct = listening_answer == "b"
    if listening_correct:
        $ day_4_listening_score += 10

    call screen day_four_listening_transcript(
        4,
        "MAN: The printer in the library is out of paper, and I need to submit this form before four.\n\nWOMAN: Why don't you use the printer in the student center? It's working, and the line was short when I passed it.\n\nMAN: I'll go there now. Thanks.",
        "Bukti: Why don't you menandai saran, dan pria menerima saran itu."
    )

    if listening_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya B. Wanita menyarankan memakai printer di student center."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Why don't you menandai suggestion secara langsung."
    elif listening_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, membeli kertas untuk printer perpustakaan."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Wanita tidak menyarankan membeli kertas. Ia menawarkan lokasi printer lain."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C, mengumpulkan formulir besok."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Formulir harus diserahkan sebelum pukul empat, jadi menunda sampai besok bertentangan dengan percakapan."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih B. Pria juga langsung berkata akan pergi ke sana."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Masalah printer diselesaikan dengan berpindah ke perangkat yang masih aktif."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Fast travel ke student center."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Jaraknya tidak cukup jauh untuk disebut fast travel."
    hide normal_speaker with day_one_speaker_swap
    if listening_correct:
        system "Jawaban benar! +10 poin. Skor sementara: [day_4_listening_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_4_listening_score]/50."

    jump day_4_listening_question_5


label day_4_listening_question_5:
    call screen day_four_listening_quiz(
        5,
        audio.day4_q5,
        "What can be inferred about the man's essay?",
        "He submitted the essay late.",
        "The professor asked him to rewrite the entire essay.",
        "It contained fewer problems than he expected."
    )
    $ listening_answer = _return
    stop listening
    $ listening_correct = listening_answer == "c"
    if listening_correct:
        $ day_4_listening_score += 10

    call screen day_four_listening_transcript(
        5,
        "WOMAN: You look relieved. Did the professor return your essay?\n\nMAN: Yes. I expected a lot of corrections, but she only marked two sentences.\n\nWOMAN: All that revising paid off, then.",
        "Bukti: expected a lot dikontraskan dengan only two; relieved menunjukkan hasil lebih baik dari perkiraan."
    )

    if listening_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya C. Esainya memiliki lebih sedikit masalah daripada yang dia perkirakan."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Kata only dan ekspresi relieved menjadi bukti utamanya."
    elif listening_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A. Mungkin esainya dikumpulkan terlambat."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Tidak ada informasi tentang keterlambatan pengumpulan."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B. Profesor memintanya menulis ulang seluruh esai."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Profesor hanya menandai dua kalimat. Itu berlawanan dengan kebutuhan menulis ulang seluruh esai."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aku memilih C. Dia mengharapkan banyak koreksi, tetapi hanya menerima dua."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Revision armor berhasil mengurangi damage."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Dan kata relieved menunjukkan hasil akhirnya lebih baik dari prediksi."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Tepat. Inference kalian berasal dari beberapa petunjuk yang saling mendukung."
    hide normal_speaker with day_one_speaker_swap
    if listening_correct:
        system "Jawaban benar! +10 poin. Skor akhir: [day_4_listening_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor akhir: [day_4_listening_score]/50."

    jump day_4_after_lesson


label day_4_after_lesson:
    play music audio.bgm_study loop fadein 0.5
    stop listening
    hide screen listening_lesson_board
    hide screen day_one_speaker_portrait
    hide normal_speaker with day_one_speaker_swap
    scene bg language laboratory with dissolve

    system "Pukul 17.15. Lima latihan Listening telah selesai."
    if 4 not in extra_practice_days:
        call screen extra_study_quiz(
            4,
            "LISTENING BONUS",
            "You hear: 'The meeting was moved to Friday because the speaker is ill.' What caused the change?",
            "The room was unavailable.",
            "The speaker is ill.",
            "The meeting finished early.",
            day_1_vocab_score + day_2_structure_score + day_3_reading_score + extra_practice_score,
            "Dengarkan hubungan sebab-akibat. Frasa because memperkenalkan alasan perubahan jadwal."
        )
        $ extra_answer = _return
        if extra_answer == "b":
            $ extra_practice_score += 10
            system "Jawaban bonus benar! +10 poin tambahan."
        else:
            system "Jawaban bonus belum tepat. Fokus pada informasi setelah because."
        $ extra_practice_days.append(4)

    system "Skor latihan Listening Hari 4: [day_4_listening_score] dari 50 poin. Bonus kumulatif: [extra_practice_score]."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    if day_4_listening_score == 50:
        leo "Lima jawaban benar. Sempurna, [player_name]. Kamu menangkap detail sekaligus fungsi ucapan tanpa bergantung pada transkrip."
        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Perfect Listening run! Telinga online seratus persen."
    elif day_4_listening_score >= 40:
        leo "Empat jawaban benar. Strategimu sudah kuat. Tinjau satu petunjuk yang terlewat."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Hasil bagus. Pertahankan fokus sampai respons terakhir."
    elif day_4_listening_score >= 30:
        leo "Tiga jawaban benar. Kamu memahami situasi umum, tetapi intent dan inference masih perlu dilatih."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Kita bisa mendengarkan ulang sambil menandai kata buktinya."
    elif day_4_listening_score >= 20:
        leo "Dua jawaban benar. Jangan mengejar setiap kata. Fokus pada masalah, perubahan, dan respons terakhir."
        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Kurangi data yang diproses, pertahankan data yang menentukan jawaban."
    else:
        leo "Skornya masih rendah, tetapi sekarang kita tahu bagian yang perlu dilatih. Mulai dari main idea dan detail sebelum masuk ke intent dan inference."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Tidak apa-apa. Setelah transkrip dibuka, kita bisa mencocokkan audio dan kalimatnya pelan-pelan."

    hide normal_speaker with day_one_speaker_swap
    system "Setelah evaluasi, Leo meminta setiap anggota menyebutkan satu kebiasaan yang akan dipakai pada latihan berikutnya."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Kalau kehilangan satu kata, aku akan terus mengikuti percakapan dan tidak berhenti panik."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku akan mencatat perubahan informasi, terutama setelah but atau actually."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aku akan membedakan arti literal dengan alasan ucapan itu disampaikan."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku tidak akan membuat cutscene tambahan saat menjawab inference."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Aku akan mencari situasi, bukti utama, lalu memeriksa respons terakhir."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Bagus. Listening bukan mengingat setiap kata. Tangkap keyword, intent, perubahan arah, dan tindakan berikutnya."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku akan mencatat nama, tempat, angka, dan waktu saja."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku juga akan menunggu parafrasa, bukan mencari kata yang sama persis di pilihan."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Strategiku adalah mencegah otak buffering saat audio berjalan."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Mulailah dengan tidak mengomentari audio saat audio sedang diputar."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Kalau kehilangan satu kata, aku harus kembali fokus pada informasi berikutnya, bukan panik."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Tepat. Tugas kalian adalah mendengarkan tiga dialog pendek, lalu mencatat keyword, intent, dan next action."
    leo "Besok kita kembali ke Structure untuk parallel structure dan reduced clauses."

    hide normal_speaker with day_one_speaker_swap
    system "Leo membagikan petunjuk tugas dan berjanji mengirim ringkasan Listening setelah makan malam."
    jump day_4_go_home


label day_4_go_home:
    play music audio.bgm_main_menu loop fadein 0.5
    stop listening
    hide normal_speaker with day_one_speaker_swap
    scene bg black with fade
    centered "{size=44}PUKUL 18.10{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "[player_name] kembali ke rumah dan meletakkan earphone di samping buku catatan."

    player "Reading memberiku waktu untuk kembali ke teks. Listening memaksaku terus mengikuti informasi yang bergerak."
    player "Yang penting bukan menangkap semuanya, tetapi mengenali bagian yang menentukan jawaban."

    if prior_backlog_day4 == 3:
        player "Rencana susulan dari Leo sudah jelas. Malam ini aku mulai dari Vocabulary selama dua puluh menit."
    elif prior_backlog_day4:
        player "Materi hari ini selesai. Aku tetap harus menyediakan waktu untuk latihan yang sebelumnya tertunda."

    jump day_4_evening_group_chat


label day_4_evening_group_chat:
    play music audio.bgm_main_menu loop fadein 0.5
    stop listening
    scene bg black with fade
    centered "{size=44}PUKUL 21.18{/size}\n{size=26}Kamar [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve

    if day_4_status == "skipped":
        system "[player_name] baru selesai membaca catatan Listening dan menyimpan rekaman latihan yang dikirim kelompok."
    else:
        system "[player_name] baru selesai mencoba satu dialog tugas dengan catatan yang dibuat sesingkat mungkin."

    with hpunch
    system "BZZT! Sebuah notifikasi dari grup Seven Days to TOEFL muncul."
    call screen whatsapp_day_four_summary_notification

    player "Ringkasan Listening dari Leo sudah masuk."
    $ day_4_group_reply = renpy.call_screen("whatsapp_day_four_summary_chat")
    call screen whatsapp_day_four_summary_followup(day_4_group_reply)
    $ day_4_summary_seen = True

    if day_4_status == "in_progress":
        $ day_4_status = "completed"

    $ current_backlog_day4 = int(day_1_makeup_pending) + int(day_2_makeup_pending) + int(day_3_makeup_pending) + int(day_4_makeup_pending)

    if day_4_status == "skipped":
        player "Terima kasih. Rekamannya akan kudengarkan dan latihan Listening susulannya akan kukerjakan."
    else:
        player "Pola listen, keywords, intent, lalu answer akan kupakai lagi saat mengerjakan tugas."

    if current_backlog_day4 >= 3:
        player "Besok aku juga harus datang pukul 14.45 untuk membahas latihan susulan bersama Leo."

    system "[player_name] memasang alarm untuk sesi Structure lanjutan, menyimpan earphone, lalu bersiap beristirahat."
    jump day_4_ending


label day_4_ending:
    stop listening
    scene bg black with fade

    if day_4_status == "skipped":
        system "Hari keempat telah berlalu. Latihan Listening susulan masih menunggu [player_name]."
    else:
        system "Hari keempat selesai. Main idea, detail, speaker intent, suggestion, dan inference telah dipelajari."

label day_4_ending_calendar:
    call screen study_calendar_day_four_to_five(
        day_one_skipped=(day_1_status == "skipped"),
        day_two_skipped=(day_2_status == "skipped"),
        day_three_skipped=(day_3_status == "skipped"),
        day_four_skipped=(day_4_status == "skipped"),
        day_one_makeup=day_1_makeup_pending,
        day_two_makeup=day_2_makeup_pending,
        day_three_makeup=day_3_makeup_pending,
        day_four_makeup=day_4_makeup_pending
    )

    $ calendar_completed_day = 4
    $ calendar_resume_label = "day_4_ending_calendar"
    $ calendar_continue_label = "day_5_afternoon"
    jump process_study_calendar


label day_5_afternoon:
    play music audio.bgm_campus loop fadein 0.5
    $ day = 5
    $ day_5_choice = ""
    $ day_5_status = "not_started"
    $ day_5_makeup_pending = False
    $ day_5_structure_score = 0
    $ day_5_summary_seen = False
    $ day_5_group_reply = ""
    $ day_5_backlog_checkin = False
    $ day_5_cleared_makeup = ""
    $ prior_backlog_day5 = int(day_1_makeup_pending) + int(day_2_makeup_pending) + int(day_3_makeup_pending) + int(day_4_makeup_pending)

    scene bg black with fade
    centered "{size=50}HARI KELIMA{/size}\n{size=30}Structure Lanjutan{/size}"

    scene bg player bedroom afternoon with fade
    show weather rain overlay
    show mc neutral at vn_center with dissolve
    system "Rabu, pukul 14.05. Hujan turun sejak siang ketika [player_name] tiba di rumah setelah kelas."
    player "Sesi hari ini dimulai pukul 15.30 di perpustakaan. Materinya parallel structure dan reduced clauses."
    system "Jalan depan mulai tergenang, tetapi informasi lalu lintas menunjukkan satu rute alternatif masih terbuka. Titik-titik air memukul jendela semakin cepat."

    with hpunch
    system "BZZT! Pesan baru masuk ke grup Seven Days to TOEFL."
    call screen whatsapp_day_five_confirmation_chat(prior_backlog_day5)

    if prior_backlog_day5 >= 3:
        player "Aku diminta datang pukul 14.45 untuk membahas latihan susulan. Berarti aku harus berangkat lebih awal meski hujan."
    elif prior_backlog_day5 == 2:
        player "Dua materi masih tertunda. Structure hari ini tidak boleh menjadi yang ketiga."
    elif prior_backlog_day5 == 1:
        player "Masih ada satu latihan susulan. Aku harus menjaga agar daftar itu tidak bertambah."
    else:
        player "Empat hari sudah kulalui tanpa latihan tertunda. Tinggal mempertahankan ritmenya."

    $ day_5_choice = renpy.call_screen("day_five_afternoon_choice")

    if day_5_choice == "skip":
        jump day_5_skip

    jump day_5_prepare


label day_5_skip:
    $ day_5_status = "skipped"
    $ day_5_makeup_pending = True
    $ current_backlog_day5 = prior_backlog_day5 + 1

    system "Genangan di jalan depan terus naik, sedangkan rute alternatif memutar cukup jauh di tengah hujan deras."
    player "Aku memilih tidak mengambil risiko terjebak di jalan. Aku harus memberi tahu mereka sekarang."
    system "[player_name] membuka grup dan menuliskan kondisi di sekitar rumah."

    call screen whatsapp_day_five_skip_chat(prior_backlog_day5, current_backlog_day5)

    player "Mereka benar. Keselamatan lebih penting, tetapi aku tetap harus bertanggung jawab pada materi yang terlewat."

    scene bg black with fade
    centered "{size=44}PUKUL 18.20{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "Hujan mulai mereda. Foto papan, lembar soal, dan catatan Structure Lanjutan sudah memenuhi percakapan grup."

    if current_backlog_day5 >= 4:
        player "Daftar susulanku sudah sangat panjang. Besok aku harus mengikuti rencana Leo tanpa menunda lagi."
    elif current_backlog_day5 >= 2:
        player "Materi yang tertunda mulai menumpuk. Malam ini aku harus menyusun urutannya, bukan sekadar merasa bersalah."
    else:
        player "Hari ini terlewat karena kondisi jalan, tetapi latihan parallel structure tetap bisa kukerjakan dari rumah."

    jump day_5_evening_group_chat


label day_5_prepare:
    play music audio.bgm_study loop fadein 0.5
    $ day_5_status = "in_progress"
    $ day_5_makeup_pending = False

    player "Hujannya deras, tetapi rute alternatif masih terbuka. Aku akan berangkat lebih awal dan tidak mengambil jalan yang tergenang."

    if day_4_status == "skipped":
        system "[player_name] memasukkan catatan Listening susulan, catatan Structure Hari 2, payung, dan alat tulis ke dalam tas."
    else:
        system "[player_name] memasukkan tugas Listening, catatan Structure Hari 2, payung, dan alat tulis ke dalam tas."

    if prior_backlog_day5 >= 3:
        scene bg black with fade
        centered "{size=44}PUKUL 14.45{/size}\n{size=26}Perpustakaan Kampus{/size}"

        scene bg library study with fade
        show weather rain overlay
        system "[player_name] tiba untuk pertemuan tambahan. Paket susulan sudah dikerjakan di rumah; Leo menyiapkan lembar itu untuk verifikasi akhir."

        show normal_speaker leo at vn_center with day_one_speaker_swap
        if day_4_backlog_plan_made:
            leo "Kita lanjutkan rencana yang dibuat kemarin. Hari ini fokus pada sesi utama; latihan lama tetap dikerjakan satu per satu sesuai urutan."
        else:
            leo "Kita tidak akan mencoba menyelesaikan seluruh backlog dalam empat puluh lima menit. Kita tentukan urutan yang realistis."

        if prior_backlog_day5 == 4:
            leo "Ada empat materi tertunda. Mulai malam ini, sediakan dua puluh menit untuk satu materi. Besok kita periksa kemajuannya sebelum Review."
        else:
            leo "Dahulukan Structure dasar sebelum Structure lanjutan, lalu lanjutkan ke materi lain berdasarkan jadwal yang sudah kita susun."

        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Baik. Aku akan mengejar satu materi secara utuh, bukan membuka semuanya lalu tidak menyelesaikan apa pun."

        $ day_5_backlog_checkin = True
        if day_4_backlog_plan_made and day_2_makeup_pending:
            $ day_5_makeup_target = "structure"
        elif day_1_makeup_pending:
            $ day_5_makeup_target = "vocabulary"
        elif day_2_makeup_pending:
            $ day_5_makeup_target = "structure"
        elif day_3_makeup_pending:
            $ day_5_makeup_target = "reading"
        else:
            $ day_5_makeup_target = "listening"

        if day_5_makeup_target == "vocabulary":
            show normal_speaker leo at vn_center with day_one_speaker_swap
            leo "Kita verifikasi paket Vocabulary yang sudah kamu kerjakan. Tunjukkan bagaimana kamu memakai context clue untuk lima kata ini."
            show normal_speaker player at vn_center with day_one_speaker_swap
            player "Aku menandai kata di sekitar target, memprediksi maknanya, lalu memeriksa apakah arti itu cocok dengan seluruh kalimat."
            system "Leo memeriksa seluruh paket, lalu meminta kalimat terakhir diperbaiki sebelum menyatakan latihan Vocabulary selesai."
            $ day_1_makeup_pending = False
            $ day_5_cleared_makeup = "Vocabulary"
        elif day_5_makeup_target == "structure":
            show normal_speaker leo at vn_center with day_one_speaker_swap
            leo "Kita verifikasi paket Structure Dasar yang sudah kamu kerjakan. Tunjukkan subject dan finite verb pada lima kalimat ini."
            show normal_speaker player at vn_center with day_one_speaker_swap
            player "Aku akan menyisihkan modifier lebih dahulu, lalu memeriksa agreement pada rangka kalimatnya."
            system "Leo memeriksa seluruh paket. Setelah satu koreksi pada relative clause, ia menyatakan latihan Structure Dasar selesai."
            $ day_2_makeup_pending = False
            $ day_5_cleared_makeup = "Structure Dasar"
        elif day_5_makeup_target == "reading":
            show normal_speaker leo at vn_center with day_one_speaker_swap
            leo "Kita verifikasi paket Reading yang sudah kamu kerjakan. Tunjukkan main idea dan bukti untuk setiap jawaban."
            show normal_speaker player at vn_center with day_one_speaker_swap
            player "Main idea harus mewakili seluruh passage, sedangkan setiap detail harus kembali ke bukti yang jelas."
            system "Leo memeriksa seluruh passage susulan dan menyatakan latihan Reading selesai setelah bukti terakhir diperbaiki."
            $ day_3_makeup_pending = False
            $ day_5_cleared_makeup = "Reading"
        else:
            show normal_speaker leo at vn_center with day_one_speaker_swap
            leo "Kita verifikasi paket Listening yang sudah kamu kerjakan. Dari semua dialog, kita putar ulang satu bagian yang paling sulit."
            show normal_speaker player at vn_center with day_one_speaker_swap
            player "Aku tidak akan mengejar setiap kata. Aku akan mengikuti perubahan informasi sampai respons terakhir."
            system "Leo mencocokkan keyword, intent, dan next action pada seluruh paket. Setelah satu replay terakhir, latihan Listening dinyatakan selesai."
            $ day_4_makeup_pending = False
            $ day_5_cleared_makeup = "Listening"

        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Satu materi sudah bisa dicoret. Sisanya tetap masuk rencana Review. Mengejar backlog berarti menguranginya satu per satu."
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Setidaknya daftar itu sekarang benar-benar berkurang."
        system "Pukul 15.20, pemeriksaan tambahan selesai tepat ketika Rina, Reza, Bima, dan Maya mulai berdatangan."
    else:
        scene bg black with fade
        centered "{size=44}PUKUL 15.20{/size}\n{size=26}Perpustakaan Kampus{/size}"

        scene bg library study with fade
        show weather rain overlay
        system "[player_name] tiba ketika hujan mulai mengecil. Meja dekat jendela telah dipenuhi lembar latihan dan stabilo warna-warni."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku sudah memesan meja ini dan menyiapkan dua warna: satu untuk bentuk yang sejajar, satu untuk yang tidak."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku membawa salinan lembar soal. Kertasnya selamat dari hujan berkat tiga lapis plastik."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku sudah membuat contoh: I like reading, to play games, and slept."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Itu bukan parallel structure. Itu kecelakaan beruntun dalam tiga bentuk verb."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Setidaknya kita langsung punya contoh kesalahan untuk diperbaiki."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Benar. Ubah menjadi reading, playing games, and sleeping. Bentuk dan fungsinya sekarang sejajar."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Kalimatnya benar, tetapi jadwal hidupku terasa diserang."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Jadwal hidupmu memang membutuhkan revisi."

    hide normal_speaker with day_one_speaker_swap
    system "Pukul 15.30, Leo berdiri di depan papan dan membagikan lembar latihan Structure Lanjutan."

    jump day_5_structure_lesson


label day_5_structure_lesson:
    play music audio.bgm_study loop fadein 0.5
    scene bg library study with dissolve
    show weather rain overlay

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Hari kelima kita kembali ke Structure. Kali ini kita akan mempelajari parallel structure dan reduced clauses."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Apakah ini masih berhubungan dengan subject, verb, dan clause dari Hari 2?"
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Sangat berhubungan. Kalian harus mengenali bentuk dan fungsi setiap bagian sebelum dapat menyejajarkan atau menyingkatnya."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Jadi materi sebelumnya menjadi parser, lalu hari ini kita melakukan optimasi."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Structure advanced dungeon telah dibuka."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Semoga tutorial Hari 2 masih tersimpan di kepalamu."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Aku siap. Selama reduced clause tidak berarti menghapus setengah kalimat secara acak."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Justru itu kesalahan yang akan kita hindari."

    if day_4_status == "skipped":
        leo "Rekaman Listening-mu tetap menjadi latihan susulan. Setelah sesi ini, kerjakan satu dialog dahulu sebelum berpindah ke materi lain."
    else:
        system "[player_name] menyerahkan catatan tiga dialog tugas Listening kepada Leo."
        leo "Catatan keyword-mu sudah cukup singkat. Aku akan memeriksa intent dan next action-nya saat kalian mengerjakan soal."

    hide normal_speaker with day_one_speaker_swap
    show screen day_five_structure_lesson_board("parallel")
    show screen day_one_speaker_portrait("leo")
    leo "Parallel structure berarti bagian-bagian yang setara memakai pola tata bahasa yang sejajar."
    leo "Pada contoh di papan, reading, taking notes, dan discussing ideas semuanya berbentuk gerund."
    show screen day_one_speaker_portrait("rina")
    rina "Jadi reading, to take notes, and discussed ideas tidak sejajar karena bentuknya berubah-ubah."
    show screen day_one_speaker_portrait("leo")
    leo "Tepat. Ketiga kegiatannya memiliki fungsi sama, jadi bentuknya juga perlu diselaraskan."
    show screen day_one_speaker_portrait("reza")
    reza "Seperti satu daftar yang mengharapkan tipe data sama."
    show screen day_one_speaker_portrait("bima")
    bima "Reading, taking notes, dan defeating grammar."
    show screen day_one_speaker_portrait("maya")
    maya "Bentuknya sejajar. Isinya masih terlalu optimistis."
    show screen day_one_speaker_portrait("leo")
    leo "Parallel tidak berarti jumlah katanya harus sama. Yang harus setara adalah pola dan fungsinya."

    hide screen day_five_structure_lesson_board
    show screen day_five_structure_lesson_board("paired")
    show screen day_one_speaker_portrait("leo")
    leo "Parallel structure juga penting pada paired conjunctions seperti both-and, either-or, neither-nor, dan not only-but also."
    leo "Bagian pertama dan kedua harus mempunyai fungsi yang sama."
    show screen day_one_speaker_portrait("player")
    player "Pada contoh, easy to use dan simple to understand sama-sama menjelaskan study guide."
    show screen day_one_speaker_portrait("leo")
    leo "Benar. Keduanya adjective phrases."
    show screen day_one_speaker_portrait("bima")
    bima "The guide is both useful and full of loot."
    show screen day_one_speaker_portrait("maya")
    maya "Secara struktur cukup sejajar. Secara akademis, buku tidak menjatuhkan loot."
    show screen day_one_speaker_portrait("leo")
    leo "Untuk ujian, periksa bentuk tepat setelah kedua bagian conjunction tersebut."

    hide screen day_five_structure_lesson_board
    show screen day_five_structure_lesson_board("relative_active")
    show screen day_one_speaker_portrait("leo")
    leo "Reduced relative clause menyingkat relative clause tanpa mengubah noun yang dijelaskannya."
    leo "Untuk makna aktif, relative pronoun dihilangkan, bentuk be juga dihilangkan jika ada, lalu verb utamanya menggunakan verb-ing."
    show screen day_one_speaker_portrait("rina")
    rina "The students who are waiting outside dapat menjadi the students waiting outside."
    show screen day_one_speaker_portrait("leo")
    leo "Benar. Students tetap menjadi pihak yang melakukan waiting."
    show screen day_one_speaker_portrait("reza")
    reza "Informasinya sama, tetapi unsur yang dapat diprediksi dihapus."
    show screen day_one_speaker_portrait("leo")
    leo "Relative pronoun harus berfungsi sebagai subject dalam relative clause. Jangan menghapus unsur secara sembarangan."

    hide screen day_five_structure_lesson_board
    show screen day_five_structure_lesson_board("relative_passive")
    show screen day_one_speaker_portrait("leo")
    leo "Jika noun menerima tindakan, gunakan past participle."
    leo "The articles that were written by Leo dapat disingkat menjadi the articles written by Leo."
    show screen day_one_speaker_portrait("player")
    player "Articles tidak melakukan writing. Articles menerima tindakan written."
    show screen day_one_speaker_portrait("leo")
    leo "Tepat. Pelaku dan penerima tindakan menentukan apakah kita memakai verb-ing atau past participle."
    show screen day_one_speaker_portrait("bima")
    bima "Kalau articles writing by Leo berarti artikelnya mengambil pena sendiri?"
    show screen day_one_speaker_portrait("maya")
    maya "Dan langsung menjadi bahan penelitian paranormal."
    show screen day_one_speaker_portrait("leo")
    leo "Karena itulah kita memeriksa makna, bukan hanya bentuk."

    hide screen day_five_structure_lesson_board
    show screen day_five_structure_lesson_board("adverb")
    show screen day_one_speaker_portrait("leo")
    leo "Adverb clause juga dapat disingkat jika subject-nya sama dengan subject pada main clause."
    leo "While Rina was walking dapat menjadi while walking karena Rina juga menjadi subject dari main clause."
    show screen day_one_speaker_portrait("rina")
    rina "Jadi dalam while walking to class, Rina reviewed her notes, orang yang berjalan dan mengulang catatan sama-sama Rina."
    show screen day_one_speaker_portrait("leo")
    leo "Benar."
    show screen day_one_speaker_portrait("bima")
    bima "Lalu apa yang salah dengan while walking to class, the rain began?"
    show screen day_one_speaker_portrait("maya")
    maya "Secara struktur, kalimat itu mengatakan bahwa hujan sedang berjalan ke kelas."
    show screen day_one_speaker_portrait("leo")
    leo "Itu disebut dangling modifier. Subject yang tersirat pada reduced clause harus sama dengan subject main clause."
    show screen day_one_speaker_portrait("reza")
    reza "Kalau subject-nya berubah, referensinya menunjuk proses yang salah."

    hide screen day_five_structure_lesson_board
    show screen day_five_structure_lesson_board("checklist")
    show screen day_one_speaker_portrait("leo")
    leo "Sebelum menjawab, periksa tiga hal: bentuk, fungsi, dan makna."
    leo "Bentuk yang terlihat sejajar masih dapat salah jika pelaku tindakannya tidak logis."
    show screen day_one_speaker_portrait("player")
    player "Untuk parallel structure aku membandingkan bagian setara. Untuk reduced clause aku mencari siapa yang melakukan atau menerima tindakan."
    show screen day_one_speaker_portrait("leo")
    leo "Tepat. Sekarang jawab lima soal. Setiap jawaban benar bernilai sepuluh poin."

    hide screen day_five_structure_lesson_board
    hide screen day_one_speaker_portrait

    jump day_5_structure_question_1


label day_5_structure_question_1:
    call screen day_five_structure_quiz(
        1,
        "During the review session, the students practiced identifying main subjects, checking verb agreement, and ___ sentence patterns.",
        "analyzed",
        "to analyze",
        "analyzing"
    )
    $ structure_answer_day5 = _return
    $ structure_correct_day5 = structure_answer_day5 == "c"

    if structure_correct_day5:
        $ day_5_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya C, analyzing. Ketiga kegiatan memakai bentuk verb-ing."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Identifying, checking, dan analyzing membentuk daftar yang sejajar."
    elif structure_answer_day5 == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, analyzed."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Analyzed berbentuk past dan memutus pola gerund pada identifying serta checking."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B, to analyze."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "To analyze adalah infinitive. Karena dua bagian sebelumnya gerund, bentuk yang sejajar adalah analyzing."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih C. Semua kegiatan setelah practiced menggunakan verb-ing."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Tiga item, satu tipe data: identifying, checking, analyzing."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Parallel combo berhasil dipertahankan."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Jangan rayakan terlalu cepat. Itu baru soal pertama."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct_day5:
        system "Jawaban benar! +10 poin. Skor sementara: [day_5_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_5_structure_score]/50."

    jump day_5_structure_question_2


label day_5_structure_question_2:
    call screen day_five_structure_quiz(
        2,
        "The new study guide is both easy to use and ___.",
        "provides clear examples",
        "simple to understand",
        "organizing the examples"
    )
    $ structure_answer_day5 = _return
    $ structure_correct_day5 = structure_answer_day5 == "b"

    if structure_correct_day5:
        $ day_5_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya B, simple to understand. Bentuk itu sejajar dengan easy to use."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Keduanya adjective phrases yang menjelaskan study guide."
    elif structure_answer_day5 == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, provides clear examples."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Setelah is both, kita membutuhkan bagian yang sejajar dengan easy to use. Provides clear examples memiliki pola berbeda."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C, organizing the examples."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Bagian itu tidak sejajar dengan easy to use dan mengubah makna kalimat. Jawabannya simple to understand."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aku memilih B. Easy to use dan simple to understand sama-sama menggambarkan kualitas buku."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Kalau memilih A, kalimatnya menjadi is both easy to use and provides, jadi polanya tidak cocok."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Buku itu mendapat dua buff: mudah digunakan dan mudah dipahami."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Untuk sekali ini, istilah buff-mu cukup membantu."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct_day5:
        system "Jawaban benar! +10 poin. Skor sementara: [day_5_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_5_structure_score]/50."

    jump day_5_structure_question_3


label day_5_structure_question_3:
    call screen day_five_structure_quiz(
        3,
        "The students ___ near the window are preparing for the Structure test.",
        "sitting",
        "who sitting",
        "are sitting"
    )
    $ structure_answer_day5 = _return
    $ structure_correct_day5 = structure_answer_day5 == "a"

    if structure_correct_day5:
        $ day_5_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya A, sitting. Bentuk lengkapnya adalah who are sitting."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Students melakukan tindakan sitting, jadi reduced clause-nya memakai verb-ing."
    elif structure_answer_day5 == "b":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B, who sitting."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Jika who dipertahankan, kita membutuhkan who are sitting. Dalam bentuk reduced, who are dihilangkan bersama-sama."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C, are sitting."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Kalimat itu sudah memiliki main verb are preparing. Are sitting tanpa relative pronoun menciptakan dua finite verbs yang tidak terhubung."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku memilih A. Who are dapat dipulihkan tanpa mengubah makna kalimat."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Students adalah pihak yang duduk, jadi bentuk aktif sitting sesuai."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Pilihan C membawa satu are terlalu banyak."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Diagnosis sederhana, tetapi benar."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct_day5:
        system "Jawaban benar! +10 poin. Skor sementara: [day_5_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_5_structure_score]/50."

    jump day_5_structure_question_4


label day_5_structure_question_4:
    call screen day_five_structure_quiz(
        4,
        "The articles ___ by the professor are available online.",
        "writing",
        "wrote",
        "written"
    )
    $ structure_answer_day5 = _return
    $ structure_correct_day5 = structure_answer_day5 == "c"

    if structure_correct_day5:
        $ day_5_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya C, written, karena articles menerima tindakan."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. That were written direduksi menjadi written."
    elif structure_answer_day5 == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, writing."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Writing memberi makna aktif seolah articles menulis sesuatu. Di sini articles ditulis oleh professor."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B, wrote."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Wrote adalah finite past verb. Reduced passive relative clause membutuhkan past participle written."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aku memilih C. Frasa by the professor juga menjadi petunjuk bahwa maknanya pasif."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Kalau jawabannya writing, artikelnya membutuhkan pena."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Atau akses keyboard. Keduanya tetap tidak menyelesaikan kesalahan grammar."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Fokus pada siapa yang melakukan dan siapa yang menerima tindakan."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct_day5:
        system "Jawaban benar! +10 poin. Skor sementara: [day_5_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor sementara: [day_5_structure_score]/50."

    jump day_5_structure_question_5


label day_5_structure_question_5:
    call screen day_five_structure_quiz(
        5,
        "Which sentence uses a reduced adverb clause correctly?",
        "While walking to class, the rain began.",
        "While walking to class, Maya reviewed her notes.",
        "While Maya walking to class, she reviewed her notes."
    )
    $ structure_answer_day5 = _return
    $ structure_correct_day5 = structure_answer_day5 == "b"

    if structure_correct_day5:
        $ day_5_structure_score += 10
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya B. Maya adalah orang yang berjalan sekaligus mengulang catatan."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Benar. Subject tersirat pada reduced clause sama dengan subject main clause."
    elif structure_answer_day5 == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "A memiliki dangling modifier. Secara struktur, kalimat itu membuat the rain menjadi pihak yang berjalan ke kelas."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Jika Maya tetap ditulis sebagai subject, kita membutuhkan while Maya was walking. Untuk bentuk reduced, gunakan while walking."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku memilih B. Pelaku walking dan reviewed sama-sama Maya."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Pilihan A membuatku membayangkan hujan berjalan masuk kelas."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Dan kemungkinan masih datang lebih tepat waktu darimu."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "B lolos pemeriksaan referensi subject. A gagal karena dangling."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Itulah alasan makna harus diperiksa setelah bentuk."

    hide normal_speaker with day_one_speaker_swap
    if structure_correct_day5:
        system "Jawaban benar! +10 poin. Skor akhir: [day_5_structure_score]/50."
    else:
        system "Jawaban belum tepat. Tidak ada tambahan poin. Skor akhir: [day_5_structure_score]/50."

    jump day_5_after_lesson


label day_5_after_lesson:
    play music audio.bgm_study loop fadein 0.5
    hide screen day_five_structure_lesson_board
    hide screen day_one_speaker_portrait
    hide normal_speaker with day_one_speaker_swap
    scene bg library study with dissolve
    show weather rain overlay

    system "Pukul 17.20. Lima latihan Structure Lanjutan telah selesai."
    if 5 not in extra_practice_days:
        call screen extra_study_quiz(
            5,
            "STRUCTURE BONUS",
            "The report was written clearly and ___ reviewed before submission.",
            "careful",
            "carefully",
            "carefulness",
            day_1_vocab_score + day_2_structure_score + day_3_reading_score + day_4_listening_score + extra_practice_score,
            "Dua kata dihubungkan oleh and. Pilih bentuk yang sejajar dengan adverb yang menerangkan reviewed."
        )
        $ extra_answer = _return
        if extra_answer == "b":
            $ extra_practice_score += 10
            system "Jawaban bonus benar! +10 poin tambahan."
        else:
            system "Jawaban bonus belum tepat. Periksa fungsi kata yang menerangkan reviewed."
        $ extra_practice_days.append(5)

    system "Skor latihan Structure Lanjutan Hari 5: [day_5_structure_score] dari 50 poin. Bonus kumulatif: [extra_practice_score]."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    if day_5_structure_score == 50:
        leo "Lima jawaban benar. Sempurna, [player_name]. Kamu menjaga kesejajaran bentuk dan mengenali reduced clause tanpa kehilangan subject-nya."
        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Advanced Structure cleared tanpa grammar damage!"
    elif day_5_structure_score >= 40:
        leo "Empat jawaban benar. Dasarmu sangat kuat. Tinjau satu pola aktif, pasif, atau parallel yang terlewat."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Bagus. Sekarang jangan mulai mengurangi semua clause yang kamu lihat."
    elif day_5_structure_score >= 30:
        leo "Tiga jawaban benar. Kamu memahami pola utamanya, tetapi masih perlu memeriksa pelaku tindakan sebelum memilih verb-ing atau past participle."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Kita bisa mengembalikan reduced clause ke bentuk lengkap saat memeriksanya."
    elif day_5_structure_score >= 20:
        leo "Dua jawaban benar. Bandingkan bagian parallel satu per satu dan selalu cari subject tersirat pada reduced clause."
        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Kembalikan bentuk singkat ke versi lengkap, lalu jalankan pemeriksaan lagi."
    else:
        leo "Skornya masih rendah, tetapi pola kesalahannya terlihat. Kita akan memisahkan latihan parallel dan reduced clause sebelum menggabungkannya."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Tidak apa-apa. Kita mulai dari daftar gerund, lalu lanjut ke active dan passive."

    hide normal_speaker with day_one_speaker_swap
    system "Leo meminta setiap anggota membuat satu contoh terakhir sebelum sesi ditutup."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "She enjoys reading, writing, and drawing."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Benar. Tiga gerund tersusun sejajar."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "The files created today are stored online."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Benar. Created today berasal dari which were created today."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "While entering the boss room, the music suddenly changed."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Masih dangling. Kalimat itu membuat music menjadi pihak yang memasuki ruangan."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Kalau begitu: While entering the boss room, the player heard the music change."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Akhirnya subject-nya berhasil masuk ke ruangan yang tepat."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Versi kedua benar."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Students preparing for the TOEFL test need consistent practice."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Bagus. Preparing for the TOEFL test menjelaskan students dan memiliki makna aktif."

    leo "Besok kita memasuki hari Review. Kalian akan menggabungkan strategi Vocabulary, Reading, Listening, dan Structure."
    system "Leo membagikan lima kalimat. Tugasnya: tandai bagian parallel, kembalikan reduced clauses ke bentuk lengkap, dan perbaiki satu dangling modifier."

    jump day_5_go_home


label day_5_go_home:
    play music audio.bgm_main_menu loop fadein 0.5
    hide normal_speaker with day_one_speaker_swap
    scene bg black with fade
    centered "{size=44}PUKUL 18.20{/size}\n{size=26}Rumah [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "[player_name] menggantung payung di dekat pintu lalu membuka kembali lembar latihan Structure Lanjutan."

    player "Parallel structure berarti fungsi yang setara membutuhkan bentuk yang sejajar. Reduced clause tetap harus mempertahankan pelaku, voice, dan makna."

    if day_5_backlog_checkin:
        player "Setidaknya latihan [day_5_cleared_makeup] sudah selesai. Backlog-ku belum hilang seluruhnya, tetapi jumlahnya benar-benar berkurang."
    elif prior_backlog_day5:
        player "Sesi hari ini tidak menambah backlog. Sekarang aku tetap harus mengikuti urutan latihan susulan yang sudah dibuat."
    else:
        player "Lima hari terlewati tanpa materi susulan. Besok tinggal menghubungkan semua strategi saat Review Terpadu."

    jump day_5_evening_group_chat


label day_5_evening_group_chat:
    play music audio.bgm_main_menu loop fadein 0.5
    scene bg black with fade
    centered "{size=44}PUKUL 21.24{/size}\n{size=26}Kamar [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve

    if day_5_status == "skipped":
        system "[player_name] baru selesai menyalin contoh parallel structure dari foto papan yang dikirim Rina."
    else:
        system "[player_name] baru selesai memperbaiki satu dangling modifier pada tugas dari Leo."

    with hpunch
    system "BZZT! Notifikasi grup Seven Days to TOEFL muncul di bagian atas layar."
    call screen whatsapp_day_five_summary_notification

    player "Ringkasan Structure Lanjutan sudah masuk."
    $ current_backlog_day5 = int(day_1_makeup_pending) + int(day_2_makeup_pending) + int(day_3_makeup_pending) + int(day_4_makeup_pending) + int(day_5_makeup_pending)
    $ day_5_group_reply = renpy.call_screen("whatsapp_day_five_summary_chat")
    call screen whatsapp_day_five_summary_followup(day_5_group_reply, current_backlog_day5)
    $ day_5_summary_seen = True

    if day_5_status == "in_progress":
        $ day_5_status = "completed"

    if day_5_status == "skipped":
        player "Catatan mereka cukup jelas untuk memulai latihan susulan. Aku harus menyelesaikannya sebelum Review Terpadu."
    else:
        player "Match form, check voice, reduce, lalu reread. Polanya jauh lebih mudah diingat setelah diringkas."

    if current_backlog_day5 >= 3:
        player "Besok aku harus datang pukul 14.45 agar satu materi susulan lagi dapat diselesaikan sebelum Review."
    elif current_backlog_day5:
        player "Masih ada latihan susulan, tetapi jumlahnya sudah bisa kutangani dengan rencana yang jelas."

    system "[player_name] memasukkan seluruh catatan lima hari ke dalam satu map untuk sesi Review besok."
    jump day_5_ending


label day_5_ending:
    scene bg black with fade

    if day_5_status == "skipped":
        system "Hari kelima telah berlalu. Latihan Structure Lanjutan masih menunggu [player_name]."
    else:
        system "Hari kelima selesai. Parallel structure, reduced relative clauses, dan dangling modifier telah dipelajari."

label day_5_ending_calendar:
    call screen study_calendar_day_five_to_six(
        day_one_skipped=(day_1_status == "skipped"),
        day_two_skipped=(day_2_status == "skipped"),
        day_three_skipped=(day_3_status == "skipped"),
        day_four_skipped=(day_4_status == "skipped"),
        day_five_skipped=(day_5_status == "skipped"),
        day_one_makeup=day_1_makeup_pending,
        day_two_makeup=day_2_makeup_pending,
        day_three_makeup=day_3_makeup_pending,
        day_four_makeup=day_4_makeup_pending,
        day_five_makeup=day_5_makeup_pending
    )

    $ calendar_completed_day = 5
    $ calendar_resume_label = "day_5_ending_calendar"
    $ calendar_continue_label = "day_6_afternoon"
    jump process_study_calendar


label day_6_afternoon:
    play music audio.bgm_cafe loop fadein 0.5
    $ day = 6
    $ day_6_status = "not_started"
    $ day_6_makeup_pending = False
    $ day_6_review_score = 0
    $ day_6_review_streak = 0
    $ day_6_travel_choice = ""
    $ day_6_drink_choice = ""
    $ day_6_backlog_checkin = False
    $ day_6_cleared_makeup = ""
    $ day_6_final_reply = ""
    $ backlog_before_day6 = int(day_1_makeup_pending) + int(day_2_makeup_pending) + int(day_3_makeup_pending) + int(day_4_makeup_pending) + int(day_5_makeup_pending)

    scene bg black with fade
    centered "{size=50}HARI KEENAM{/size}\n{size=30}Review Terpadu di Kafe{/size}"

    scene bg player bedroom afternoon with fade
    show mc neutral at vn_center with dissolve
    system "Kamis, pukul 13.50. Cahaya siang masuk melalui jendela kamar [player_name]; hujan kemarin hanya menyisakan genangan tipis di tepi jalan."

    if day_5_status == "skipped":
        player "Kemarin jalan keluar kompleks tertutup air. Hari ini cuacanya jauh lebih bersahabat. Aku tidak akan berdebat lagi dengan hujan."
    else:
        player "Jalan yang kemarin kulewati di tengah hujan sekarang sudah tenang. Hari ini semoga kepala kami juga ikut tenang."

    player "Semua catatan lima hari sudah masuk satu map. Tinggal memastikan lokasi dan perlengkapannya."

    with hpunch
    system "BZZT! Grup Seven Days to TOEFL mengirim pembaruan mendadak."
    call screen whatsapp_day_six_location_update(backlog_before_day6)

    player "Kafe Ruang Sela, seberang gerbang timur. Perubahan lokasi yang sangat disukai Bima dan sangat dicurigai Maya."

    if backlog_before_day6 >= 3:
        player "Check-in pukul 14.45 tetap berjalan. Aku harus membawa paket susulan yang sudah kukerjakan dan berangkat sekarang."
    elif backlog_before_day6:
        player "Masih ada [backlog_before_day6] materi susulan. Hari ini aku akan mencatat bagian yang paling perlu diprioritaskan tanpa mencoba menelan semuanya sekaligus."
    else:
        player "Tidak ada latihan susulan yang tertinggal. Hari ini aku bisa fokus menghubungkan semua strategi."

    system "[player_name] memasukkan map catatan, earphone, pensil, penghapus, dan botol air ke dalam tas."
    hide mc with dissolve

    $ day_6_travel_choice = renpy.call_screen("day_six_travel_choice", backlog_before_day6)
    $ day_6_status = "in_progress"

    if backlog_before_day6 < 3:
        scene bg player bedroom afternoon with dissolve
        show mc neutral at vn_center with dissolve
        system "Setelah menentukan rute, [player_name] memakai waktu satu jam untuk makan ringan, beristirahat, dan memeriksa isi tas sekali lagi—tanpa membuka materi baru."
        player "Rutenya sudah dipilih. Aku berangkat pukul 14.50 supaya tidak perlu terburu-buru."
        hide mc with dissolve

    jump day_6_travel


label day_6_travel:
    play music audio.bgm_campus loop fadein 0.5
    scene bg day6 journey afternoon with fade

    if backlog_before_day6 >= 3:
        system "Pukul 14.20. [player_name] menyeberangi kawasan kampus lebih awal. Aspal yang masih lembap memantulkan cahaya keemasan di bawah pepohonan."
    else:
        system "Pukul 14.55. [player_name] berjalan dari gerbang timur menuju deretan kafe kecil di tepi kampus. Udara setelah hujan terasa lebih sejuk."

    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Perjalanan singkat seperti ini ternyata cukup membantu. Lima hari terakhir rasanya selalu berpindah dari catatan ke papan lalu kembali ke catatan."

    if day_6_travel_choice == "park":
        system "Di persimpangan jalur taman, Rina dan Maya terlihat mengejar selembar sticky note yang diterbangkan angin."

        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "[player_name], tolong tangkap yang warna hijau! Itu catatan reduced clause-ku!"

        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Dapat. Isinya cuma tulisan V-ing dengan tiga garis bawah."

        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Setidaknya modifier itu akhirnya menemukan subject yang benar."

        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Aku memilih jalur taman supaya sebelum Review kita sempat bernapas. Di kafe nanti tidak boleh langsung membuka lima buku sekaligus."

        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Setuju. Kalau semua catatan dibuka sekaligus, meja kita berubah jadi lokasi bencana akademik."

        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Dan Bima akan menyebutnya inventory management. Ayo berangkat sebelum prediksi itu menjadi nyata."
    else:
        system "Di trotoar jalan utama, Reza sedang memeriksa pin lokasi sementara Bima memegang ponselnya terbalik."

        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Bima, panahnya menunjuk ke belakang karena ponselmu terbalik. Kita sedang menjauhi kafe."

        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Aku hanya sedang membuka bagian peta yang belum terjelajahi."

        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Bagian yang belum terjelajahi itu bernama jalan pulang. Kafenya ke arah gerbang timur."

        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Rute sudah dihitung ulang. Jika kita mengikuti [player_name], peluang tiba di lokasi yang benar naik drastis."

        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Baiklah. Party leader sementara dipindahkan. Aku tetap bertanggung jawab atas moral support."

        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Mulailah dengan memegang ponselnya dalam orientasi yang benar."

    hide normal_speaker with day_one_speaker_swap

    if backlog_before_day6 >= 3:
        system "Rute yang dipilih membawa [player_name] ke Kafe Ruang Sela pukul 14.40, lima menit sebelum check-in."
    else:
        system "Mereka tiba pukul 15.12. Dari balik jendela kafe, meja kayu panjang yang dipesan Rina sudah terlihat."

    jump day_6_cafe_arrival


label day_6_cafe_arrival:
    play music audio.bgm_cafe loop fadein 0.5
    scene bg black with fade
    if backlog_before_day6 >= 3:
        centered "{size=44}PUKUL 14.40{/size}\n{size=26}Kafe Ruang Sela{/size}"
    else:
        centered "{size=44}PUKUL 15.12{/size}\n{size=26}Kafe Ruang Sela{/size}"

    scene bg day6 cafe afternoon with fade
    system "Cahaya sore yang masih terang masuk melalui jendela Kafe Ruang Sela. Di meja untuk enam orang, Rina sudah menyiapkan beberapa pilihan minuman, kartu kosong, dan sepiring kecil dessert."
    system "Musik lo-fi terdengar pelan, bercampur aroma kopi dan roti panggang."

    if backlog_before_day6 >= 3:
        $ day_6_backlog_checkin = True
        system "Teman-teman yang ikut tiba lebih awal memilih minuman di dekat kasir dan memberi ruang di ujung meja saat Leo membuka paket susulan [player_name]."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Kamu datang tepat waktu. Kita tidak akan mengulang satu hari penuh di sini; paket lengkapnya sudah kamu kerjakan di rumah. Sekarang kita lakukan verifikasi akhir."

        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku membawa seluruh jawabannya dan menandai bagian yang masih membuatku ragu."

        if day_2_makeup_pending and day_5_makeup_pending:
            $ day_6_makeup_target = "structure_basic"
        elif day_1_makeup_pending:
            $ day_6_makeup_target = "vocabulary"
        elif day_2_makeup_pending:
            $ day_6_makeup_target = "structure_basic"
        elif day_3_makeup_pending:
            $ day_6_makeup_target = "reading"
        elif day_4_makeup_pending:
            $ day_6_makeup_target = "listening"
        else:
            $ day_6_makeup_target = "structure_advanced"

        if day_6_makeup_target == "vocabulary":
            show normal_speaker leo at vn_center with day_one_speaker_swap
            leo "Kita periksa paket Vocabulary: lima context clues dan lima kalimat buatanmu. Jelaskan mengapa arti yang dipilih cocok dengan keseluruhan kalimat."
            show normal_speaker player at vn_center with day_one_speaker_swap
            player "Aku memakai kata penanda kontras, sebab-akibat, dan contoh. Satu arti kuubah setelah membaca ulang konteks paragrafnya."
            system "Leo memeriksa seluruh paket, mengoreksi satu collocation, lalu menyatakan latihan Vocabulary selesai."
            $ day_1_makeup_pending = False
            $ day_6_cleared_makeup = "Vocabulary"
        elif day_6_makeup_target == "structure_basic":
            show normal_speaker leo at vn_center with day_one_speaker_swap
            leo "Structure Dasar harus kuat sebelum Structure Lanjutan. Tunjukkan subject, finite verb, dan agreement pada lima kalimat paketmu."
            show normal_speaker player at vn_center with day_one_speaker_swap
            player "Aku menyisihkan prepositional phrase lebih dulu, lalu mencocokkan subject utama dengan verb-nya."
            system "Leo memeriksa lima kalimat lengkap. Setelah satu relative clause diperbaiki, latihan Structure Dasar dinyatakan selesai."
            $ day_2_makeup_pending = False
            $ day_6_cleared_makeup = "Structure Dasar"
        elif day_6_makeup_target == "reading":
            show normal_speaker leo at vn_center with day_one_speaker_swap
            leo "Untuk Reading, tunjukkan main idea dan bukti dua supporting details pada setiap passage susulan."
            show normal_speaker player at vn_center with day_one_speaker_swap
            player "Aku menulis nomor baris di samping tiap jawaban supaya kesimpulannya tidak lepas dari teks."
            system "Leo menelusuri seluruh jawaban dan meminta satu inference dipersempit. Paket Reading kemudian dinyatakan selesai."
            $ day_3_makeup_pending = False
            $ day_6_cleared_makeup = "Reading"
        elif day_6_makeup_target == "listening":
            show normal_speaker leo at vn_center with day_one_speaker_swap
            leo "Paket Listening-mu berisi tiga dialog. Kita putar ulang bagian tersulit, lalu cocokkan keyword, intent, dan next action untuk semuanya."
            show normal_speaker player at vn_center with day_one_speaker_swap
            player "Aku mengikuti koreksi informasi dan respons terakhir, bukan berusaha menangkap setiap kata."
            system "Setelah seluruh lembar bukti diperiksa dan satu replay terakhir selesai, latihan Listening dinyatakan tuntas."
            $ day_4_makeup_pending = False
            $ day_6_cleared_makeup = "Listening"
        else:
            show normal_speaker leo at vn_center with day_one_speaker_swap
            leo "Kita verifikasi lima transformasi Structure Lanjutan: dua parallel structures, dua reduced clauses, dan satu dangling modifier."
            show normal_speaker player at vn_center with day_one_speaker_swap
            player "Aku mengembalikan reduced clause ke bentuk lengkap sebelum memeriksa active atau passive voice-nya."
            system "Leo memeriksa kelima transformasi. Setelah bentuk paralel terakhir diselaraskan, latihan Structure Lanjutan dinyatakan selesai."
            $ day_5_makeup_pending = False
            $ day_6_cleared_makeup = "Structure Lanjutan"

        $ backlog_after_checkin_day6 = int(day_1_makeup_pending) + int(day_2_makeup_pending) + int(day_3_makeup_pending) + int(day_4_makeup_pending) + int(day_5_makeup_pending)

        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Satu paket, [day_6_cleared_makeup], selesai secara utuh. Masih ada [backlog_after_checkin_day6] materi tertunda; itu daftar prioritas, bukan alasan untuk panik."

        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku akan mengikuti urutannya. Tidak ada lagi membuka semua paket lalu tidak menyelesaikan satu pun."

        system "Pukul 15.20, check-in berakhir. Teman yang menunggu kembali ke meja, sementara anggota lain datang dan melengkapi kelompok."
    else:
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Kalian datang lebih awal. Aku sengaja tidak membawa papan tulis. Hari ini semua materi akan bergerak di atas meja melalui kartu-kartu kecil."

        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Bagus. Otakku mulai mengira setiap pertemuan harus diawali kapur dan garis bawah."

    if day_6_travel_choice == "park":
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Meja sudah siap. Sticky note hijau juga selamat berkat [player_name]."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Sementara itu, Reza dan Bima akhirnya tiba tanpa membuka area peta baru."
        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Kami hanya mengambil rute dengan bonus eksplorasi."
        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Bonusnya adalah dua kali putar balik."
    else:
        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Kami tiba berkat koreksi orientasi peta dari [player_name]."
        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Aku sedang menguji ketahanan party terhadap navigasi dinamis."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Untung meja kami tidak ikut berpindah."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Jangan beri dia peta saat simulasi besok."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Sebelum mulai, pilih salah satu minuman yang sudah dipesan Rina dan duduk dengan nyaman. Review yang baik tidak harus terasa seperti hukuman."

    hide normal_speaker with day_one_speaker_swap
    $ day_6_drink_choice = renpy.call_screen("day_six_cafe_drink_choice")

    if day_6_drink_choice == "tea":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku pilih teh lemon hangat. Aku butuh kepala yang tenang, bukan tambahan detak jantung."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Pilihan paling masuk akal di meja ini."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Aku menyetujui bagian hangatnya, tetapi cokelat tetap minuman healing resmi."
    elif day_6_drink_choice == "chocolate":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Cokelat panas. Hari ini judulnya healing, jadi aku mengikuti tema."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Pilihan resmi panitia pemulihan energi!"
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Panitianya baru dibentuk lima detik lalu dan hanya beranggotakan Rina."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Es kopi susu. Semoga ini menjadi patch untuk RAM-ku."
        show normal_speaker reza at vn_center with day_one_speaker_swap
        reza "Patch diterima. Jangan jalankan terlalu banyak proses setelah pukul sepuluh malam."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Dan jangan menganggap kafein sebagai pengganti tidur."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Kalau begitu aku pesan tiga espresso. Satu untuk Vocabulary, satu Structure, satu—"

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Satu saja. Besok kami membutuhkanmu sadar, bukan bergetar."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Tutor kita mulai mengatur status effect pemain."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Karena pemainnya tidak memiliki pengaturan keselamatan sendiri."

    jump day_6_integrated_review


label day_6_integrated_review:
    play music audio.bgm_cafe loop fadein 0.5
    scene bg day6 cafe afternoon with dissolve
    system "Pukul 15.30, enam gelas sudah berada di atas coaster dan Leo membagi lima amplop warna-warni di tengah meja."
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Hari ini kita tidak mengulang lima hari dari awal. Kita akan menghubungkan strategi yang sudah kalian pelajari."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Lima hari lalu aku panik hanya karena membaca pengumuman TOEFL. Sekarang setidaknya aku bisa menjelaskan mengapa satu pilihan salah."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Kapasitas RAM kelompok meningkat secara bertahap."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Perkembangan. Masih berisik, tetapi sudah berkembang."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Ini campfire terakhir sebelum final boss."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Untuk sekali ini, perumpamaanmu tepat. Ada lima kartu tantangan. Setiap jawaban benar bernilai sepuluh poin."
    leo "Setelah kartu ketiga kita mengambil jeda delapan menit. Tidak ada papan, tidak ada sesi ceramah panjang, dan tidak ada hukuman jika perlu berpikir."

    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Lima kartu, empat kemampuan, satu meja yang wangi kopi. Aku siap."

    hide normal_speaker with day_one_speaker_swap
    system "Rina mengocok lima amplop warna-warni lalu mendorong amplop hijau ke tengah meja."

    jump day_6_challenge_1


label day_6_challenge_1:
    play music audio.bgm_quiz loop fadein 0.3 volume 0.3
    call screen day_six_cafe_challenge(
        1,
        "CONTEXT HUNT",
        "VOCABULARY",
        "Although Maya had expected the review to be exhausting, the quiet music and warm drink made the session surprisingly restorative. What is the closest meaning of restorative?",
        "Causing confusion",
        "Helping someone recover energy or well-being",
        "Requiring intense concentration",
        "Perhatikan kontras antara exhausting dan hasil setelah musik serta minuman.",
        False
    )
    $ day_6_answer = _return
    $ day_6_correct = day_6_answer == "b"
    if day_6_correct:
        $ day_6_review_score += 10
        $ day_6_review_streak += 1
    else:
        $ day_6_review_streak = 0

    call screen day_six_challenge_result(
        1,
        "CONTEXT HUNT",
        day_6_correct,
        "Although menandai kontras: sesi diperkirakan melelahkan, tetapi musik dan minuman membantu memulihkan kondisi. Restorative berarti membantu memulihkan tenaga atau well-being."
    )

    if day_6_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya B. Restorative berarti membantu memulihkan tenaga atau kondisi."
    elif day_6_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, causing confusion."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C, requiring intense concentration."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Kuncinya B. Although menghubungkan ekspektasi exhausting dengan hasil yang justru membuat sesi terasa memulihkan."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku menandai Although dan warm drink. Konteksnya bergerak dari lelah menuju pulih."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Jadi restorative adalah healing buff. Kamus Bima akhirnya diakui."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Untuk istilah itu saja, terjemahanmu lolos pemeriksaan."

    hide normal_speaker with day_one_speaker_swap
    system "Reza membuka amplop biru dan meletakkan tiga potongan kalimat seperti kepingan puzzle."
    jump day_6_challenge_2


label day_6_challenge_2:
    play music audio.bgm_quiz loop fadein 0.3 volume 0.3
    call screen day_six_cafe_challenge(
        2,
        "SENTENCE REPAIR",
        "STRUCTURE",
        "Leo asked the group to review key words, identify sentence patterns, and ___ evidence carefully.",
        "checking",
        "checked",
        "check",
        "Bandingkan bentuk setelah to: review, identify, dan bagian yang kosong.",
        False
    )
    $ day_6_answer = _return
    $ day_6_correct = day_6_answer == "c"
    if day_6_correct:
        $ day_6_review_score += 10
        $ day_6_review_streak += 1
    else:
        $ day_6_review_streak = 0

    call screen day_six_challenge_result(
        2,
        "SENTENCE REPAIR",
        day_6_correct,
        "Kata to dipakai bersama oleh tiga base verbs: review, identify, dan check. Ketiga tindakan memiliki fungsi dan bentuk yang sejajar."
    )

    if day_6_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya C, check. Review, identify, dan check semuanya base verb."
    elif day_6_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, checking."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B, checked."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Jawaban yang sejajar adalah C. Satu kata to mengendalikan tiga base verbs dalam daftar yang sama."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Tiga elemen dengan tipe yang sama. Parser kalimatnya tidak perlu melakukan konversi bentuk."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Parallel combo masih aktif."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Selama kamu tidak menambahkan defeated di akhir daftar."

    hide normal_speaker with day_one_speaker_swap
    system "Maya membalik amplop merah muda. Di dalamnya ada satu passage pendek dan tiga kartu main idea."
    jump day_6_challenge_3


label day_6_challenge_3:
    play music audio.bgm_quiz loop fadein 0.3 volume 0.3
    call screen day_six_reading_challenge(
        3,
        "CATATAN TENTANG JEDA BELAJAR",
        day_six_reading_passage,
        "Which option best states the main idea of the passage?",
        "Planned short breaks can restore focus, while unlimited breaks may become avoidance.",
        "Learners should avoid taking breaks during difficult tasks.",
        "Every study session should stop whenever a learner feels tired.",
        "Main idea harus mencakup manfaat jeda sekaligus batas yang dijelaskan penulis."
    )
    $ day_6_answer = _return
    $ day_6_correct = day_6_answer == "a"
    if day_6_correct:
        $ day_6_review_score += 10
        $ day_6_review_streak += 1
    else:
        $ day_6_review_streak = 0

    call screen day_six_challenge_result(
        3,
        "EVIDENCE SCAN",
        day_6_correct,
        "Pilihan A mencakup dua sisi passage: jeda singkat yang direncanakan dapat mengembalikan fokus, sedangkan jeda tanpa batas dapat menjadi penghindaran. B dan C terlalu mutlak."
    )

    if day_6_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya A. Pilihan itu merangkum manfaat jeda dan risikonya bila tidak dibatasi."
    elif day_6_answer == "b":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B karena passage membahas tugas sulit."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C karena passage menyebut mental fatigue."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Kuncinya A. B menolak semua jeda, sedangkan C menyuruh berhenti setiap kali lelah. Keduanya lebih mutlak daripada teks."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "A mencakup seluruh passage, bukan hanya kalimat tentang manfaat."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Berarti healing juga memerlukan batas waktu agar tidak berubah menjadi menghindari soal."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Tepat. Karena itu sekarang kita menerapkan passage tersebut: jeda delapan menit."

    hide normal_speaker with day_one_speaker_swap
    scene bg day6 cafe sunset with dissolve
    system "Leo membalik timer kecil. Selama delapan menit, semua kartu ditutup dan tidak seorang pun boleh membahas jawaban."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aturan jeda: minum, makan satu potong dessert, dan lihat keluar jendela."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Kalau dua potong dessert? Itu masih satu aktivitas."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Kamu baru saja menemukan loophole delapan detik setelah aturan dibuat."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Timer berjalan. Perdebatan dessert mengonsumsi 6,25 persen waktu istirahat."

    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Untuk pertama kalinya minggu ini, kami duduk bersama tanpa buru-buru mencari subject, keyword, atau main idea."

    system "Musik kafe mengisi jeda. Di luar, cahaya sore perlahan berubah jingga dan percakapan mereka beralih ke makanan, game, serta tugas kampus yang tidak berkaitan dengan TOEFL."
    system "Delapan menit kemudian, cahaya di jendela mulai menghangat menuju jingga. Leo hanya mengetuk amplop keempat sekali; semua kembali ke meja tanpa perlu dipanggil dua kali."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Fokus kalian terlihat lebih baik. Kartu keempat adalah audio recall: satu rekaman Hari 4 kita pilih kembali untuk menguji suggestion dan respons terakhir."

    hide normal_speaker with day_one_speaker_swap
    jump day_6_challenge_4


label day_6_challenge_4:
    stop music fadeout 0.5
    call screen day_six_listening_challenge(
        4,
        audio.day4_q4,
        "What does the woman suggest the man do?",
        "Buy paper for the library printer",
        "Use the printer in the student center",
        "Submit the form the following day"
    )
    $ day_6_answer = _return
    stop listening
    $ day_6_correct = day_6_answer == "b"
    if day_6_correct:
        $ day_6_review_score += 10
        $ day_6_review_streak += 1
    else:
        $ day_6_review_streak = 0

    call screen day_four_listening_transcript(
        4,
        "MAN: The printer in the library is out of paper, and I need to submit this form before four.\n\nWOMAN: Why don't you use the printer in the student center? It's working, and the line was short when I passed it.\n\nMAN: I'll go there now. Thanks.",
        "Bukti: Why don't you menandai suggestion, dan I'll go there now mengonfirmasi tindakan berikutnya."
    )

    call screen day_six_challenge_result(
        4,
        "AUDIO RECALL",
        day_6_correct,
        "Why don't you menandai saran untuk memakai printer di student center. Respons I'll go there now mengonfirmasi bahwa saran tersebut diterima."
    )

    if day_6_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya B. Wanita menyarankan memakai printer di student center."
    elif day_6_answer == "a":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih A, membeli kertas untuk printer perpustakaan."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C, mengumpulkan formulir besok."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Kuncinya B. Suggestion muncul setelah Why don't you, lalu diterima melalui I'll go there now."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku memilih B karena printer aktif adalah resource utama party."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Bukti utamanya tetap saran dan respons terakhir, bukan resource party."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku kehilangan kata passed, tetapi itu tidak menghalangi informasi penentunya."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Bagus. Kehilangan satu kata tidak berarti kehilangan seluruh dialog."

    hide normal_speaker with day_one_speaker_swap
    system "Bima mengangkat amplop emas terakhir seperti hendak membuka hadiah langka."
    jump day_6_challenge_5


label day_6_challenge_5:
    play music audio.bgm_quiz loop fadein 0.3 volume 0.3
    call screen day_six_cafe_challenge(
        5,
        "FINAL COMBO",
        "MIXED",
        "To keep the shared room comfortable, visitors are asked to speak quietly, keep tables clean, and ___ phone calls outside. These rules are intended to minimize disruptions. Which option correctly completes the sentence and gives the meaning of minimize?",
        "take; minimize means reduce",
        "take; minimize means increase",
        "taking; minimize means reduce",
        "Periksa parallel structure setelah asked to, lalu gunakan tujuan aturan untuk menafsirkan minimize.",
        True
    )
    $ day_6_answer = _return
    $ day_6_correct = day_6_answer == "a"
    if day_6_correct:
        $ day_6_review_score += 10
        $ day_6_review_streak += 1
    else:
        $ day_6_review_streak = 0

    call screen day_six_challenge_result(
        5,
        "FINAL COMBO",
        day_6_correct,
        "Speak, keep, dan take adalah base verbs sejajar setelah asked to. Dari tujuan menjaga kenyamanan, minimize berarti mengurangi gangguan. Jawaban yang menghubungkan kedua strategi adalah A."
    )

    if day_6_correct:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Jawabannya A. Take sejajar dengan speak dan keep, sedangkan minimize berarti reduce."
    elif day_6_answer == "b":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih B, take dan increase."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku memilih C, taking dan reduce."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Kuncinya A. Satu soal meminta kalian memeriksa bentuk kalimat dan makna kata dari tujuan teks."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Structure memvalidasi take. Konteks kalimat kedua memvalidasi reduce. Dua pemeriksaan, satu jawaban."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Kalau minimize berarti increase, aturan itu justru akan menambah gangguan dan bertentangan dengan comfortable."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Final combo selesai. Amplop emasnya tidak menjatuhkan loot, tetapi aku tetap puas."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Peningkatan terbesarmu hari ini adalah menerima bahwa kertas tidak menjatuhkan loot."

    jump day_6_after_review


label day_6_after_review:
    play music audio.bgm_hopeful loop fadein 0.5
    hide normal_speaker with day_one_speaker_swap
    scene bg day6 cafe evening with dissolve
    $ day_6_status = "completed"
    $ remaining_backlog_day6 = int(day_1_makeup_pending) + int(day_2_makeup_pending) + int(day_3_makeup_pending) + int(day_4_makeup_pending) + int(day_5_makeup_pending)

    system "Pukul 17.20. Lima amplop sudah terbuka dan cahaya di luar jendela mulai memudar."
    system "Skor Review Terpadu Hari 6: [day_6_review_score] dari 50 poin."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    if day_6_review_score == 50:
        leo "Lima jawaban benar. Kamu berhasil menghubungkan context clue, parallel structure, main idea, listening cues, dan strategi campuran tanpa kehilangan bukti."
    elif day_6_review_score >= 40:
        leo "Empat jawaban benar. Kesiapanmu sangat kuat. Tinjau satu bukti yang terlewat, lalu berhenti."
    elif day_6_review_score >= 30:
        leo "Tiga jawaban benar. Dasarmu stabil. Tandai dua pola kesalahan untuk ditinjau malam ini, bukan seluruh buku."
    elif day_6_review_score >= 20:
        leo "Dua jawaban benar. Fokuskan review pada pembahasan yang salah dan alasan jawabannya. Membaca semuanya lagi hanya akan menambah beban."
    else:
        leo "Skornya belum tinggi, tetapi malam ini bukan waktu untuk cramming. Tinjau pembahasan lima kartu, siapkan perlengkapan, lalu tidur cukup."

    if remaining_backlog_day6:
        leo "Masih ada [remaining_backlog_day6] materi susulan yang tercatat. Gunakan itu sebagai daftar fokus jangka pendek, bukan alasan untuk panik sebelum simulasi."
    else:
        leo "Tidak ada materi susulan yang tertinggal. Pertahankan ritme itu sampai simulasi selesai."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku jauh lebih tenang daripada saat membawa pengumuman itu ke kantin. Sekarang soal salah pun terasa bisa dibongkar satu per satu."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Review hari ini seperti integration test. Komponen terpisah akhirnya berjalan dalam satu alur."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Aku mengakui kelompok ini ternyata tidak sepenuhnya tidak efisien."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Kami datang sebagai random party dan pulang sebagai party yang tahu role masing-masing."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Mengajari kalian juga membantuku. Beberapa hal yang kuanggap sederhana ternyata baru jelas setelah harus kujelaskan dengan langkah kecil."

    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Skor satu latihan penting, tetapi cara kami saling melengkapi terasa lebih besar daripada angka itu."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Besok simulasi dimulai pukul 08.00 di Laboratorium Bahasa. Datang pukul 07.40, bawa pensil, penghapus, earphone, dan air minum."

    if remaining_backlog_day6 >= 3:
        leo "[player_name], datang pukul 07.20 untuk briefing singkat. Kita tidak akan cramming; kita hanya memastikan strategi prioritasmu."

    leo "Malam ini jangan mencari materi baru. Tinjau soal yang salah, berhenti belajar pukul 22.00, lalu tidur."

    hide normal_speaker with day_one_speaker_swap
    $ day_6_final_reply = renpy.call_screen("day_six_readiness_choice")

    if day_6_final_reply == "practical":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Peralatan dan alarm sudah siap. Besok aku datang tepat waktu."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Bagus. Tambahkan sarapan ke checklist-mu. Konsentrasi juga membutuhkan energi."
        show normal_speaker rina at vn_center with day_one_speaker_swap
        rina "Aku akan kirim pengingat satu kali saja. Tidak ada spam pukul lima pagi."
    elif day_6_final_reply == "honest":
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Aku masih gugup, tetapi aku akan mempercayai latihan enam hari ini."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Gugup tidak menghapus persiapanmu. Besok kembali saja ke strategi ketika satu soal terasa sulit."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Dan ingat, satu soal aneh bukan ramalan untuk seluruh hasil."
    else:
        show normal_speaker player at vn_center with day_one_speaker_swap
        player "Tolong larang Bima menyebut simulasi sebagai final boss setiap lima menit."
        show normal_speaker bima at vn_center with day_one_speaker_swap
        bima "Baik. Aku ganti menjadi ultimate assessment encounter."
        show normal_speaker maya at vn_center with day_one_speaker_swap
        maya "Permohonan ditolak. Kembali ke final boss, maksimal satu kali besok pagi."
        show normal_speaker leo at vn_center with day_one_speaker_swap
        leo "Aku tidak menyangka harus menambahkan batas penggunaan metafora ke aturan simulasi."

    system "Rina lalu menyandarkan ponsel pada tumpukan buku dan mengaktifkan timer kamera."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Satu foto sebelum pulang. Bukan untuk nilai, hanya bukti bahwa kita pernah belajar tanpa wajah panik."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Pose kemenangan party!"

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Berdiri normal selama tiga detik. Itu tantangan keenammu."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Kenapa aku harus ikut?"

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Karena tanpa tutor, dataset fotonya tidak lengkap."

    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Terlambat menolak, Leo. Timer-nya sudah berjalan."

    hide normal_speaker with day_one_speaker_swap
    with hpunch
    system "Klik! Foto menangkap enam orang, lima amplop kosong, minuman yang hampir habis, dan Bima yang tetap mengangkat dua jari seperti baru menamatkan permainan."

    jump day_6_journey_home


label day_6_journey_home:
    play music audio.bgm_hopeful loop fadein 0.5
    scene bg black with fade
    centered "{size=44}PUKUL 17.48{/size}\n{size=26}Perjalanan Pulang{/size}"

    scene bg day6 journey evening with fade
    system "Mereka meninggalkan Kafe Ruang Sela bersama. Lampu toko mulai menyala dan jalan yang basah memantulkan warna jingga terakhir dari langit."

    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Secara resmi hari ini kita belajar, healing, makan dessert, dan tidak ada yang tumbang. Sesi terbaik."

    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Kamu hampir tumbang karena mencoba minum espresso terlalu cepat."

    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Foto grupnya bagus. Aku kirim setelah sampai rumah—tanpa stiker berlebihan."

    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku sudah membuat salinan cadangan. Pengalaman Hari 4 mengajarkan bahwa file penting tidak boleh hanya berada di satu perangkat."

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Sampai besok pagi. Setelah tiba di rumah, hanya periksa tas dan dua kesalahan utama. Tidak lebih."

    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Enam hari lalu kami bahkan belum memiliki rencana. Besok kami akan melihat sejauh apa latihan ini membawa kami."

    hide normal_speaker with day_one_speaker_swap
    system "Di persimpangan, mereka berpisah satu per satu. Untuk pertama kalinya menjelang ujian, langkah [player_name] pulang terasa lebih ringan daripada saat berangkat."
    system "[player_name] tiba di rumah sekitar pukul 18.25, lalu mandi, makan malam, dan beristirahat. Ia baru kembali ke meja belajar setelah tubuhnya terasa segar."

    scene bg black with fade
    centered "{size=44}PUKUL 20.45{/size}\n{size=26}Kamar [player_name]{/size}"

    scene bg player bedroom with fade
    show mc neutral at vn_center with dissolve
    system "Di rumah, [player_name] menaruh pensil, penghapus, earphone, kartu peserta, dan botol air dalam satu baris di atas meja."
    player "Tidak ada materi baru. Hanya periksa kesalahan hari ini, pasang alarm, lalu tidur."

    if remaining_backlog_day6:
        player "Masih ada [remaining_backlog_day6] latihan susulan, tetapi malam ini tugasku bukan menyelesaikan semuanya. Simulasi besok tetap membutuhkan tubuh dan pikiran yang cukup istirahat."
    else:
        player "Tidak ada latihan susulan yang tertinggal. Sekarang tantangannya adalah berhenti belajar tepat waktu."

    system "[player_name] menutup map setelah dua pembahasan, memasang alarm, dan meletakkan ponsel jauh dari bantal."

    jump day_6_ending


label day_6_ending:
    hide mc with dissolve
    scene bg black with fade
    system "Hari keenam selesai. Vocabulary, Structure, Reading, dan Listening telah dihubungkan melalui Review Terpadu di Kafe Ruang Sela."

label day_6_ending_calendar:
    call screen study_calendar_day_six_to_seven(
        day_one_skipped=(day_1_status == "skipped"),
        day_two_skipped=(day_2_status == "skipped"),
        day_three_skipped=(day_3_status == "skipped"),
        day_four_skipped=(day_4_status == "skipped"),
        day_five_skipped=(day_5_status == "skipped"),
        day_six_skipped=(day_6_status == "skipped"),
        day_one_makeup=day_1_makeup_pending,
        day_two_makeup=day_2_makeup_pending,
        day_three_makeup=day_3_makeup_pending,
        day_four_makeup=day_4_makeup_pending,
        day_five_makeup=day_5_makeup_pending,
        day_six_makeup=day_6_makeup_pending
    )

    $ calendar_completed_day = 6
    $ calendar_resume_label = "day_6_ending_calendar"
    $ calendar_continue_label = "day_7_morning"
    jump process_study_calendar


label day_7_morning:
    play music audio.bgm_exam loop fadein 0.5
    $ day = 7
    $ day_7_status = "in_progress"
    $ day_7_exam_score = 0
    $ day_7_exam_question = 0
    $ day_7_face_scanned = False
    $ day_7_room_scanned = False
    $ day_7_cheating_detected = False
    $ day_7_cheating_items = []
    $ day_7_used_items = []

    scene bg black with fade
    centered "{size=50}HARI KETUJUH{/size}\n{size=30}Simulasi TOEFL dan Evaluasi Akhir{/size}"

    scene bg player bedroom morning with fade
    show mc neutral at vn_center with dissolve
    system "Pukul 06.00. Hari ujian akhirnya tiba. [player_name] memeriksa meja belajar untuk memastikan tidak ada perlengkapan penting yang tertinggal."
    $ day_7_packed_items = renpy.call_screen("study_desk_inventory", title_text="HARI UJIAN  •  PILIH PERLENGKAPAN")
    player "Kartu identitas, buku catatan, pensil, dan ponsel sudah aman. Aku siap berangkat."

    scene bg day7 exam classroom with fade
    show mc neutral at vn_center with dissolve
    system "Pukul 07.35. [player_name] tiba di depan ruang kelas simulasi. Beberapa peserta lain sedang memeriksa nomor meja."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Pagi, [player_name]. Aku sudah membaca ulang catatan Listening, tetapi telapak tanganku tetap berkeringat."
    hide normal_speaker with day_one_speaker_swap
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Ini bukan boss fight biasa. Kali ini arena-nya punya pengawas dan timer resmi."
    hide normal_speaker with day_one_speaker_swap
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Tarik napas. Kita sudah mengulang strategi selama enam hari. Jangan biarkan satu soal membuatmu lupa semua latihan."
    hide normal_speaker with day_one_speaker_swap
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku membawa pensil cadangan, penghapus, dan... tiga permen untuk keadaan darurat akademik."
    hide normal_speaker with day_one_speaker_swap
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Kita masuk bersama. Baca instruksi, ikuti prosedur, lalu kerjakan satu soal pada satu waktu."
    hide normal_speaker with day_one_speaker_swap

    teacher "Selamat pagi. Saya Ibu Diah, pengawas simulasi hari ini. Sebelum duduk, dengarkan prosedurnya sampai selesai."
    teacher "Pertama, letakkan kartu identitas di sisi kiri meja. Kedua, keluarkan hanya barang yang memang ingin digunakan."
    teacher "Ketiga, scan wajah dan ruangan dilakukan melalui aplikasi ujian. Selama ujian, ponsel tetap berada di meja dan tidak boleh membuka aplikasi lain."
    teacher "Keempat, setiap soal harus dijawab sebelum berpindah. Jika skor akhir belum mencapai target 400, cerita tetap berlanjut sampai semua soal selesai dan hasil evaluasi muncul."
    player "Baik, Bu. Saya mengerti."

    $ day_7_class_items = renpy.call_screen("day7_unpack_inventory_visual", day_7_packed_items)
    $ day_7_used_items = renpy.call_screen("day7_pre_scan_item_use", day_7_class_items)
    # Setelah dikonfirmasi digunakan, barang berpindah dari meja ke tangan/player
    # sehingga tidak lagi terlihat pada kamera scan ruangan.
    $ day_7_class_items = [item for item in day_7_class_items if item not in day_7_used_items]
    system "Perlengkapan telah ditata. Pengawas meminta semua peserta melakukan verifikasi identitas dan ruangan."

    $ day_7_face_scanned = renpy.call_screen("day7_face_scan_englishscore")
    $ day_7_scanned_points = []
    $ day_7_room_scanned = renpy.call_screen("day7_room_camera_scan", day_7_class_items)
    # Kamera menyimpan temuan secara diam-diam; peringatan baru muncul di hasil akhir.
    $ day_7_cheating_items = day7_detect_cheating(day_7_class_items)
    $ day_7_cheating_detected = bool(day_7_cheating_items)

    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Sekarang buka aplikasi ujian pada ponsel. Tiga sesi akan menguji 20 soal Vocabulary dan Grammar, 20 soal Reading, lalu 20 soal Listening."
    hide normal_speaker with day_one_speaker_swap

    $ day_7_previous_score = day_1_vocab_score + day_2_structure_score + day_3_reading_score + day_4_listening_score + day_5_structure_score + day_6_review_score + extra_practice_score
    $ day_7_exam_question = 0

label day_7_exam_loop:
    if day_7_exam_question >= len(day_7_exam_questions):
        jump day_7_exam_complete

    if day_7_exam_question == 40:
        stop music fadeout 0.5
    elif day_7_exam_question == 0:
        play music audio.bgm_quiz loop fadein 0.3 volume 0.3

    if day_7_exam_question == 20:
        scene bg day7 exam desk with dissolve
        teacher "Sesi pertama Vocabulary dan Grammar selesai. Ambil napas sebentar, tetapi tetap di meja. Sekarang lanjut ke Reading."
        player "Aku akan mencari main idea dan bukti detail seperti latihan Hari 3."
    elif day_7_exam_question == 40:
        scene bg day7 exam desk with dissolve
        teacher "Sesi Reading selesai. Pastikan headset dan volume siap. Sesi terakhir adalah Listening."
        player "Keyword, perubahan informasi, dan respons terakhir. Aku ingat urutannya."

    $ day_7_question_data = day_7_exam_questions[day_7_exam_question]
    $ day_7_audio_file = day7_audio_for_question(day_7_exam_question)
    $ day_7_time_limit = day7_question_time(day_7_question_data[0])
    call screen day7_exam_question_phone(
        day_7_exam_question + 1,
        len(day_7_exam_questions),
        day_7_question_data[0],
        day_7_question_data[1],
        day_7_question_data[2],
        day_7_question_data[3],
        day_7_question_data[4],
        day_7_previous_score,
        day_7_question_data[6],
        day_7_audio_file,
        day_7_time_limit
    )
    $ day_7_answer = _return
    if day_7_answer == day_7_question_data[5]:
        $ day_7_exam_score += 10
    $ day_7_exam_question += 1
    jump day_7_exam_loop


label day_7_exam_complete:
    play music audio.bgm_exam loop fadein 0.5
    $ day_7_final_score = day_7_previous_score + day_7_exam_score
    $ day_7_status = "completed"
    $ day_7_ending = day7_ending_title(day_7_exam_score, day_7_final_score, day_7_cheating_detected)

    scene bg day7 exam classroom with dissolve
    system "Semua 60 soal sudah dijawab. Tidak ada sesi yang dipotong meskipun skor sementara belum mencapai target."
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Aku lega. Bagian Reading terasa panjang, tetapi strategi main idea membantu menjaga fokus."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Aku hampir memakai seluruh timer untuk Grammar. Untung aplikasi memberi peringatan sebelum waktu habis."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Listening terakhir cukup cepat, tetapi keyword dan respons terakhir masih bisa ditangkap."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku menyelesaikan semua soal tanpa menjatuhkan ponsel. Itu sudah termasuk achievement pribadi."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Sekarang kita tunggu pengumuman resminya. Apa pun hasilnya, setidaknya semua latihan sudah benar-benar diuji."
    hide normal_speaker with day_one_speaker_swap

    scene bg black with fade
    centered "{size=48}BEBERAPA HARI KEMUDIAN{/size}\n{size=28}Pengumuman hasil simulasi telah tersedia{/size}"
    scene bg cafeteria with dissolve
    show normal_speaker leo at vn_center with day_one_speaker_swap
    leo "Hasil sudah masuk. Kita periksa bersama agar setiap orang tahu bagian yang perlu dipertahankan dan diperbaiki."
    hide normal_speaker with day_one_speaker_swap
    show normal_speaker rina at vn_center with day_one_speaker_swap
    rina "Hasilku paling tinggi di Listening. Ternyata mencatat perubahan informasi benar-benar membantu."
    show normal_speaker bima at vn_center with day_one_speaker_swap
    bima "Grammar-ku masih naik turun, tetapi Vocabulary bonus menyelamatkan banyak poin."
    show normal_speaker maya at vn_center with day_one_speaker_swap
    maya "Reading-ku stabil karena aku memaksa diri mencari bukti, bukan memilih jawaban yang terdengar bagus."
    show normal_speaker reza at vn_center with day_one_speaker_swap
    reza "Aku akan merayakan bagian yang benar dulu sebelum membaca daftar error. Dengan dessert, tentu saja."
    show normal_speaker player at vn_center with day_one_speaker_swap
    player "Aku ingin melihat total dan rincian tiap sesi. Setelah itu kita bisa membicarakan langkah berikutnya bersama."
    hide normal_speaker with day_one_speaker_swap

    call screen day7_final_result(day_7_final_score, day_7_exam_score, day_7_final_score >= target_score and not day_7_cheating_detected, day_7_ending, day_7_cheating_detected, day_7_cheating_items)

    scene bg black with fade
    if day_7_cheating_detected and day_7_exam_score >= 500:
        play music audio.bgm_violation loop fadein 0.5
        centered "{size=48}ENDING X{/size}\n{size=28}Nilai Tinggi, Terdeteksi Curang{/size}"
        player "Nilainya tinggi, tetapi kamera menemukan barang yang tidak boleh terlihat. Hasil ini tidak bisa dianggap sah."
        system "Prosedur anti-kecurangan membatalkan kelulusan simulasi."
    elif day_7_cheating_detected and day_7_final_score >= target_score:
        play music audio.bgm_violation loop fadein 0.5
        centered "{size=48}ENDING Y{/size}\n{size=28}Lulus Skor, Terdeteksi Curang{/size}"
        player "Aku melewati 400 poin, tetapi pemeriksaan ruangan menemukan perlengkapan terlarang."
        system "Skor dicatat sebagai tidak lulus karena pelanggaran prosedur."
    elif day_7_cheating_detected:
        play music audio.bgm_violation loop fadein 0.5
        centered "{size=48}ENDING Z{/size}\n{size=28}Tidak Lulus dan Terdeteksi Curang{/size}"
        player "Skorku belum mencapai 400 dan hasil scan juga menunjukkan pelanggaran prosedur."
        system "Study Group membantuku menyusun rencana belajar dan mengulang ujian secara jujur."
    elif day_7_exam_score >= 500:
        play music audio.bgm_master loop fadein 0.5
        centered "{size=48}ENDING S{/size}\n{size=28}Master Strategist{/size}"
        player "Semua sesi terasa terukur. Aku bukan hanya melewati target, tetapi memahami cara memperbaiki kesalahan."
        system "Leo mengusulkan [player_name] menjadi mentor latihan untuk angkatan berikutnya."
    elif day_7_final_score >= target_score:
        play music audio.bgm_hopeful loop fadein 0.5
        centered "{size=48}ENDING A{/size}\n{size=28}Lulus di Atas 400{/size}"
        player "Target tercapai, tetapi beberapa sesi masih perlu kuperbaiki sebelum ujian resmi."
        system "Leo menyimpan daftar review tambahan agar peningkatan tidak berhenti di angka 400."
    else:
        play music audio.bgm_hopeful loop fadein 0.5
        centered "{size=48}ENDING C{/size}\n{size=28}Belum Lulus, Tetap Berproses{/size}"
        player "Skorku belum mencapai target, tetapi sekarang aku tahu kesalahan mana yang harus diperbaiki."
        system "Study Group sepakat melanjutkan latihan sampai [player_name] siap mengikuti simulasi berikutnya."

    # Simpan ending ke galeri pencapaian dan tandai seluruh save run ini selesai.
    $ ending_record = dict(getattr(persistent, "ending_gallery", {}) or {})
    $ ending_record[day_7_ending] = {"score": day_7_final_score, "exam_score": day_7_exam_score, "player_name": player_name, "cheating": day_7_cheating_detected}
    $ persistent.ending_gallery = ending_record
    $ completed_record = dict(getattr(persistent, "completed_story_runs", {}) or {})
    $ completed_record[story_run_id] = day_7_ending
    $ persistent.completed_story_runs = completed_record
    $ renpy.save_persistent()

label day_7_ending_review_panel:
    call screen day7_review_panel(day_7_final_score, day_7_exam_score, day_7_ending, day_7_cheating_detected, day_7_cheating_items)
    $ calendar_completed_day = 7
    $ calendar_resume_label = "day_7_ending_review_panel"
    $ calendar_continue_label = "day_7_ending_done"
    jump process_study_calendar

label day_7_ending_done:
    return


label process_study_calendar:
    if _return == "review":
        call screen study_day_review(day_number=calendar_completed_day)
        jump expression calendar_resume_label

    if _return == "switch":
        call screen study_day_switcher_all(current_day=calendar_completed_day)
        $ selected_day = selected_study_day(_return)
        if selected_day is None:
            jump expression calendar_resume_label
        if selected_day <= calendar_completed_day:
            call screen study_day_review(day_number=selected_day)
            jump expression calendar_resume_label
        $ selected_label = story_day_label(selected_day)
        if selected_label:
            jump expression selected_label
        jump expression calendar_resume_label

    jump expression calendar_continue_label
