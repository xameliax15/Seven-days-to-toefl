################################################################################
## Inisialisasi
################################################################################

init offset = -1


################################################################################
## Screen khusus prolog Seven Days to TOEFL
################################################################################

transform whatsapp_message_fade(delay=0.0):
    alpha 0.0
    yoffset 12
    pause delay
    easeout 0.35 alpha 1.0 yoffset 0


transform whatsapp_system_event_fade(delay=0.0):
    alpha 0.0
    yoffset 9
    pause delay
    easeout 0.30 alpha 1.0 yoffset 0


transform whatsapp_notification_pop:
    alpha 0.0
    yoffset -38
    easeout 0.24 alpha 1.0 yoffset 0
    pause 1.05
    easeout 0.22 alpha 0.0 yoffset -20


transform whatsapp_followup_enter:
    alpha 0.0
    yoffset 20
    easeout 0.25 alpha 1.0 yoffset 0


transform whatsapp_evening_chat_scroll:
    yoffset 0
    pause 3.75
    easeout 0.40 yoffset -130
    pause 1.35
    easeout 0.40 yoffset -300
    pause 1.15
    easeout 0.35 yoffset -380


transform calendar_scene_fade:
    alpha 0.0
    linear 0.25 alpha 1.0


transform calendar_strip_shift:
    xoffset 0
    pause 1.05
    ease 0.80 xoffset -328


transform calendar_complete_stamp:
    alpha 0.0
    zoom 1.25
    pause 0.50
    easeout 0.25 alpha 1.0 zoom 1.0


transform calendar_old_caption:
    alpha 1.0
    pause 1.15
    easeout 0.25 alpha 0.0 yoffset -12


transform calendar_new_caption:
    alpha 0.0
    yoffset 12
    pause 1.55
    easeout 0.30 alpha 1.0 yoffset 0


transform calendar_active_badge:
    alpha 0.0
    zoom 1.15
    pause 1.75
    easeout 0.25 alpha 1.0 zoom 1.0


transform calendar_progress_fill:
    xanchor 0.0
    xzoom 0.0
    pause 1.55
    easeout 0.45 xzoom 1.0


transform calendar_progress_day_two:
    xanchor 0.0
    xzoom 0.5
    pause 1.55
    easeout 0.45 xzoom 1.0


transform calendar_progress_day_three:
    xanchor 0.0
    xzoom 0.6667
    pause 1.55
    easeout 0.45 xzoom 1.0


transform calendar_progress_day_four:
    xanchor 0.0
    xzoom 0.75
    pause 1.55
    easeout 0.45 xzoom 1.0


transform calendar_progress_day_five:
    xanchor 0.0
    xzoom 0.8
    pause 1.55
    easeout 0.45 xzoom 1.0


transform calendar_progress_day_six:
    xanchor 0.0
    xzoom 0.8333
    pause 1.55
    easeout 0.45 xzoom 1.0


transform calendar_progress_day_seven:
    xanchor 0.0
    xzoom 0.8571
    pause 1.55
    easeout 0.45 xzoom 1.0


transform day_six_panel_enter:
    alpha 0.0
    yoffset 18
    zoom 0.97
    easeout 0.25 alpha 1.0 yoffset 0 zoom 1.0


transform day_six_card_enter(delay=0.0):
    alpha 0.0
    xoffset 22
    pause delay
    easeout 0.24 alpha 1.0 xoffset 0


transform day_six_cup_float:
    yoffset 0
    ease 1.20 yoffset -6
    ease 1.20 yoffset 0
    repeat


transform vocabulary_board_enter:
    alpha 0.0
    yoffset -16
    easeout 0.28 alpha 1.0 yoffset 0


transform vocabulary_chalk_appear(delay=0.0):
    alpha 0.0
    xoffset -14
    pause delay
    easeout 0.30 alpha 1.0 xoffset 0


transform lesson_speaker_card_enter:
    alpha 0.0
    xoffset 36
    pause 0.05
    easeout 0.25 alpha 1.0 xoffset 0


init python:
    def day_one_speaker_portrait_data(speaker):
        if speaker == "player":
            portrait = "images/m_player.png" if player_gender == "male" else "images/f_player.png"
            return portrait, player_name, "PEMAIN", "#22d3ee"

        portraits = {
            "leo": ("images/leo.png", "Leo", "TUTOR", "#c4b5fd"),
            "rina": ("images/rina.png", "Rina", "ANGGOTA KELOMPOK", "#34d399"),
            "reza": ("images/reza.png", "Reza", "ANGGOTA KELOMPOK", "#fbbf24"),
            "bima": ("images/bima.png", "Bima", "ANGGOTA KELOMPOK", "#60a5fa"),
            "maya": ("images/maya.png", "Maya", "ANGGOTA KELOMPOK", "#f472b6"),
        }

        return portraits[speaker]

    def story_save_slots(limit=1):
        """Mengembalikan satu save cerita utama beserta metadata pemain.

        Slot kosong diisi None agar layar selalu memiliki tiga kartu yang
        konsisten. Metadata player_name dan player_gender berasal dari
        config.save_json_callbacks di options.rpy.
        """
        try:
            saved = renpy.list_saved_games(
                regexp=r"^story-main$", fast=False
            )
        except Exception:
            saved = []

        # Urutan tuple Ren'Py: (slot_name, extra_info, thumbnail, save_time).
        # Indeks 2 adalah gambar screenshot, bukan nilai waktu.
        saved = sorted(saved, key=lambda item: item[3], reverse=True)[:limit]
        result = []
        for slot_name, extra_info, thumbnail, save_time in saved:
            try:
                metadata = renpy.slot_json(slot_name) or {}
            except Exception:
                metadata = {}

            completed_runs = getattr(persistent, "completed_story_runs", {}) or {}
            if metadata.get("story_run_id") in completed_runs:
                # Semua save dari run yang sudah mencapai ending dianggap selesai.
                continue

            gender = metadata.get("player_gender", "-")
            if gender == "male":
                gender = "Laki-laki"
            elif gender == "female":
                gender = "Perempuan"

            result.append({
                "slot": slot_name,
                "name": metadata.get("player_name", extra_info or "Pemain"),
                "gender": gender,
                "portrait": "images/m_player.png" if metadata.get("player_gender") == "male" else "images/f_player.png",
                "time": save_time,
                "thumbnail": thumbnail,
            })

        while len(result) < limit:
            result.append(None)
        return result


screen player_name_input():
    modal True
    default entered_name = ""

    add Solid("#050812")
    add Solid("#071b2b") alpha 0.78

    frame:
        xalign 0.5
        yalign 0.5
        xsize 760
        padding (48, 42)
        background Frame(Solid("#102638e8"), 2, 2)

        vbox:
            spacing 24
            text "IDENTITAS PEMAIN" size 18 color "#22d3ee" xalign 0.5
            text "Masukkan nama Anda" size 38 color "#f8fafc" xalign 0.5
            text "Nama ini akan digunakan sepanjang permainan." size 18 color "#94a3b8" xalign 0.5

            frame:
                xfill True
                padding (20, 14)
                background Solid("#06131fcc")
                input:
                    value ScreenVariableInputValue("entered_name")
                    length 18
                    allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-"
                    size 28
                    color "#ffffff"
                    caret Solid("#22d3ee", xsize=3)
                    xalign 0.5

            textbutton "MULAI PROLOG  →":
                xalign 0.5
                sensitive bool(entered_name.strip())
                action Return(entered_name.strip())
                padding (30, 14)
                background Solid("#0891b2")
                hover_background Solid("#06b6d4")
                insensitive_background Solid("#334155")
                text_color "#ffffff"
                text_size 22

    key "K_RETURN" action If(bool(entered_name.strip()), Return(entered_name.strip()), NullAction())


screen player_gender_selection():
    modal True
    zorder 100

    add Solid("#050812")
    add Solid("#071b2b") alpha 0.78

    vbox:
        xalign 0.5
        ypos 34
        spacing 8

        text "IDENTITAS KARAKTER" size 18 color "#22d3ee" xalign 0.5
        text "Pilih karakter [player_name]" size 38 bold True color "#f8fafc" xalign 0.5
        text "Pilihan ini menentukan tampilan karakter utama selama permainan." size 19 color "#94a3b8" xalign 0.5

    hbox:
        xalign 0.5
        ypos 180
        spacing 70

        button:
            xsize 560
            ysize 790
            padding (24, 22)
            background Solid("#0f2338ee")
            hover_background Solid("#164e63")
            action Return("male")

            vbox:
                xalign 0.5
                spacing 10

                fixed:
                    xsize 512
                    ysize 610
                    add Transform("images/m_player.png", xysize=(400, 600)):
                        xalign 0.5
                        yalign 1.0

                text "LAKI-LAKI" size 34 bold True color "#67e8f9" xalign 0.5
                text "Pilih karakter ini" size 18 color "#cbd5e1" xalign 0.5

        button:
            xsize 560
            ysize 790
            padding (24, 22)
            background Solid("#28172dee")
            hover_background Solid("#4a2148")
            action Return("female")

            vbox:
                xalign 0.5
                spacing 10

                fixed:
                    xsize 512
                    ysize 610
                    add Transform("images/f_player.png", xysize=(400, 600)):
                        xalign 0.5
                        yalign 1.0

                text "PEREMPUAN" size 34 bold True color "#f9a8d4" xalign 0.5
                text "Pilih karakter ini" size 18 color "#e2e8f0" xalign 0.5


screen whatsapp_announcement():
    modal True
    zorder 100
    default can_dismiss = False

    add Solid("#000000b8")

    fixed at screen_shake:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "17:30" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Info Akademik FTI UNIBBA" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "Grup WhatsApp • 128 anggota" xpos 158 ypos 119 size 15 color "#d7f2ec"

        text "HARI INI" xpos 316 ypos 190 size 15 bold True color "#55706a"

        fixed at whatsapp_message_fade(0.25):
            xpos 47
            ypos 224
            xsize 583
            ysize 250

            add "gui/whatsapp_chat_bubble.svg"
            text "Admin Prodi" xpos 41 ypos 19 size 19 bold True color "#17856f"
            text "{b}PENGUMUMAN PENTING{/b}\nMengingat evaluasi akademik semester ini, Tes Simulasi Kemahiran Bahasa Inggris sebagai syarat wajib pendaftaran Sidang Skripsi akan dimajukan menjadi {b}MINGGU DEPAN{/b}." xpos 41 ypos 55 xsize 510 size 20 color "#17251d" line_spacing 5
            text "17:30  ✓✓" xpos 475 ypos 216 size 14 color "#73827d"

        fixed at whatsapp_message_fade(0.95):
            xpos 47
            ypos 483
            xsize 583
            ysize 229

            add Transform("gui/whatsapp_chat_bubble.svg", xysize=(583, 229))
            text "Seluruh mahasiswa wajib mencapai skor minimum {b}{color=#b91c1c}400 (Standar Minimum TOEFL ITP){/color}{/b}.\nHarap persiapkan diri masing-masing. Tidak ada ujian susulan bagi mahasiswa yang tidak hadir." xpos 41 ypos 29 xsize 510 size 20 color "#17251d" line_spacing 5
            text "17:30  ✓✓" xpos 475 ypos 195 size 14 color "#73827d"

        text "Ketik pesan" xpos 121 ypos 895 size 20 color "#82938e"

    timer 1.45 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_member_event(event_text, event_y, event_delay):
    fixed at whatsapp_system_event_fade(event_delay):
        xpos 72
        ypos event_y
        xsize 546
        ysize 54

        text "+" xpos 4 ypos 4 size 26 bold True color "#128c7e"
        text event_text xpos 46 ypos 8 xsize 480 size 18 color "#49645c" text_align 0.5
        add Solid("#78968d2b") xpos 46 ypos 50 xsize 455 ysize 1


screen whatsapp_group_setup():
    modal True
    zorder 100

    add Solid("#000000b8")

    fixed at screen_shake:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "17:42" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"

        text "HARI INI" xpos 316 ypos 190 size 15 bold True color "#55706a"

        use whatsapp_member_event("Maya membuat grup 'Seven Days to TOEFL'", 235, 0.25)
        use whatsapp_member_event("Maya menambahkan Rina", 302, 0.78)
        use whatsapp_member_event("Maya menjadikan Rina sebagai admin grup", 369, 1.31)
        use whatsapp_member_event("Rina menambahkan Anda", 436, 1.84)
        use whatsapp_member_event("Rina menambahkan Leo", 503, 2.37)
        use whatsapp_member_event("Rina menambahkan Reza", 570, 2.90)
        use whatsapp_member_event("Rina menambahkan Bima", 637, 3.43)
        use whatsapp_member_event("Maya menjadikan Anda sebagai admin grup", 704, 3.96)

        text "Ketik pesan" xpos 121 ypos 895 size 20 color "#82938e"

    timer 4.75 action Return(True)
    key "dismiss" action Return(True)


screen whatsapp_evening_notification():
    modal True
    zorder 120

    frame at whatsapp_notification_pop:
        xalign 0.5
        ypos 54
        xsize 740
        ysize 126
        padding (20, 14)
        background Solid("#101827f2")

        hbox:
            spacing 18

            fixed:
                xsize 82
                ysize 82
                add Solid("#128c7e")
                text "WA" xalign 0.5 yalign 0.5 size 27 bold True color "#ffffff"

            vbox:
                xsize 590
                spacing 3
                text "WHATSAPP  •  SEKARANG" size 16 bold True color "#76d8c9"
                text "Seven Days to TOEFL" size 25 bold True color "#ffffff"
                text "Maya: Besok pukul 08.00 di perpustakaan, semua bisa?" xsize 570 size 19 color "#d9e4e8"

    timer 1.60 action Return(True)


screen whatsapp_group_text_message(sender, message, message_y, bubble_width, bubble_height, message_delay, sender_color="#128c7e", outgoing=False):
    fixed at whatsapp_message_fade(message_delay):
        xpos (610 - bubble_width if outgoing else 0)
        ypos message_y
        xsize bubble_width
        ysize bubble_height

        if outgoing:
            add Transform("gui/whatsapp_bubble_outgoing.svg", xysize=(bubble_width, bubble_height))
        else:
            add Transform("gui/whatsapp_bubble_incoming.svg", xysize=(bubble_width, bubble_height))

        text sender:
            xpos 22
            ypos 9
            size 16
            bold True
            color sender_color

        text message:
            xpos 22
            ypos 32
            xsize (bubble_width - 44)
            size 19
            color "#17251d"
            line_spacing 2


screen whatsapp_evening_chat():
    modal True
    zorder 100
    default can_dismiss = False

    add Solid("#000000b8")

    fixed at screen_shake:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "20:41" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        viewport:
            xpos 40
            ypos 215
            xsize 610
            ysize 650
            draggable False
            mousewheel False

            fixed:
                xsize 610
                ysize 1040

                fixed at whatsapp_evening_chat_scroll:
                    xsize 610
                    ysize 1040

                    use whatsapp_group_text_message(
                        "Maya",
                        "Besok pukul 08.00 di perpustakaan kampus. Semua bisa?",
                        0, 470, 90, 0.25, "#7e57c2"
                    )

                    use whatsapp_group_text_message(
                        "Rina",
                        "Aku bisa. Alarm sudah kupasang.",
                        100, 390, 75, 0.95, "#d94683"
                    )

                    use whatsapp_group_text_message(
                        "Reza",
                        "Tubuhku bisa hadir jam delapan. Kesadaranku mungkin menyusul jam sembilan.",
                        185, 500, 100, 1.65, "#2563eb"
                    )

                    use whatsapp_group_text_message(
                        "Bima",
                        "Aku siap! Mental juga sudah siap!",
                        295, 410, 78, 2.35, "#ea6a16"
                    )

                    fixed at whatsapp_message_fade(3.05):
                        xpos 12
                        ypos 383
                        xsize 215
                        ysize 205

                        text "Bima" xpos 10 ypos 0 size 16 bold True color "#ea6a16"
                        add Transform("gui/sticker_sleepy_cat_8am.png", xysize=(185, 185)) xpos 8 ypos 20

                    use whatsapp_group_text_message(
                        "Leo",
                        "Jadwal diterima. Bima, stiker bukan jawaban jadwal.",
                        598, 470, 88, 4.05, "#00897b"
                    )

                    use whatsapp_group_text_message(
                        "Bima",
                        "Itu laporan kesiapan mental dalam format visual, Pak Guru.",
                        696, 500, 88, 4.85, "#ea6a16"
                    )

                    use whatsapp_group_text_message(
                        "Anda",
                        "Rekap besok: 08.00, Perpustakaan Kampus. Materi: Vocabulary. Bawa alat tulis dan semangat hidup.",
                        794, 520, 120, 5.65, "#128c7e", True
                    )

                    use whatsapp_group_text_message(
                        "Maya",
                        "Rekap diterima. Semoga semangat hidup Reza datang tepat waktu.",
                        924, 500, 98, 6.45, "#7e57c2"
                    )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Ketik pesan" xpos 121 ypos 895 size 20 color "#82938e"

    timer 7.60 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen day_one_morning_choice():
    modal True
    zorder 110

    add Solid("#020617b8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        padding (54, 46)
        background Solid("#0b1f2eef")

        vbox:
            spacing 30

            vbox:
                xalign 0.5
                spacing 7
                text "HARI 1  •  06.45" xalign 0.5 size 19 bold True color "#67e8f9"
                text "Apa yang akan kamu lakukan?" xalign 0.5 size 42 bold True color "#f8fafc"
                text "Pilihanmu menentukan kegiatan [player_name] hari ini." xalign 0.5 size 21 color "#a9bdc9"

            hbox:
                xalign 0.5
                spacing 36

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#3d2027ee")
                    hover_background Solid("#7f1d2d")
                    action Return("skip")

                    vbox:
                        spacing 14
                        text "01" size 21 bold True color "#fda4af"
                        text "SKIP HARI INI" size 36 bold True color "#fff1f2"
                        add Solid("#fb7185") xsize 110 ysize 4
                        text "Kirim izin ke grup dan beristirahat di rumah." xsize 480 size 23 color "#fecdd3"
                        text "Hari 1 akan ditandai sebagai dilewati." size 18 color "#fda4af"

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#123a42ee")
                    hover_background Solid("#0e7490")
                    action Return("prepare")

                    vbox:
                        spacing 14
                        text "02" size 21 bold True color "#67e8f9"
                        text "BERSIAP-SIAP" size 36 bold True color "#ecfeff"
                        add Solid("#22d3ee") xsize 110 ysize 4
                        text "Datang ke perpustakaan dan ikuti sesi Vocabulary." xsize 480 size 23 color "#cffafe"
                        text "Selesaikan latihan pada sesi pertama." size 18 color "#67e8f9"


screen day_two_morning_choice():
    modal True
    zorder 110

    add Solid("#020617b8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        padding (54, 46)
        background Solid("#0b1f2eef")

        vbox:
            spacing 30

            vbox:
                xalign 0.5
                spacing 7
                text "HARI 2  •  06.45" xalign 0.5 size 19 bold True color "#67e8f9"
                text "Apa yang akan kamu lakukan?" xalign 0.5 size 42 bold True color "#f8fafc"
                text "Kelompok menunggu di perpustakaan pukul 08.00." xalign 0.5 size 21 color "#a9bdc9"

            hbox:
                xalign 0.5
                spacing 36

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#3d2027ee")
                    hover_background Solid("#7f1d2d")
                    action Return("skip")

                    vbox:
                        spacing 14
                        text "01" size 21 bold True color "#fda4af"
                        text "SKIP HARI INI" size 36 bold True color "#fff1f2"
                        add Solid("#fb7185") xsize 110 ysize 4
                        text "Kirim izin ke grup dan lewati sesi Structure." xsize 480 size 23 color "#fecdd3"
                        text "Latihan susulan akan ditambahkan." size 18 color "#fda4af"

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#123a42ee")
                    hover_background Solid("#0e7490")
                    action Return("prepare")

                    vbox:
                        spacing 14
                        text "02" size 21 bold True color "#67e8f9"
                        text "BERSIAP-SIAP" size 36 bold True color "#ecfeff"
                        add Solid("#22d3ee") xsize 110 ysize 4
                        text "Berangkat ke perpustakaan dan belajar Structure." xsize 480 size 23 color "#cffafe"
                        text "Bawa tugas Vocabulary dan alat tulis." size 18 color "#67e8f9"


screen day_three_afternoon_choice():
    modal True
    zorder 110

    add Solid("#020617b8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        padding (54, 46)
        background Solid("#0b1f2eef")

        vbox:
            spacing 30

            vbox:
                xalign 0.5
                spacing 7
                text "HARI 3  •  14.20" xalign 0.5 size 19 bold True color "#67e8f9"
                text "Apa yang akan kamu lakukan?" xalign 0.5 size 42 bold True color "#f8fafc"
                text "Kelompok bertemu di perpustakaan pukul 15.30." xalign 0.5 size 21 color "#a9bdc9"

            hbox:
                xalign 0.5
                spacing 36

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#3d2027ee")
                    hover_background Solid("#7f1d2d")
                    action Return("skip")

                    vbox:
                        spacing 14
                        text "01" size 21 bold True color "#fda4af"
                        text "SKIP HARI INI" size 36 bold True color "#fff1f2"
                        add Solid("#fb7185") xsize 110 ysize 4
                        text "Kirim izin ke grup dan lewati sesi Reading." xsize 480 size 23 color "#fecdd3"
                        text "Latihan susulan akan ditambahkan." size 18 color "#fda4af"

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#123a42ee")
                    hover_background Solid("#0e7490")
                    action Return("prepare")

                    vbox:
                        spacing 14
                        text "02" size 21 bold True color "#67e8f9"
                        text "BERSIAP-SIAP" size 36 bold True color "#ecfeff"
                        add Solid("#22d3ee") xsize 110 ysize 4
                        text "Berangkat dan belajar strategi Reading." xsize 480 size 23 color "#cffafe"
                        text ("Bawa catatan Structure susulan dan alat tulis." if day_2_status == "skipped" else "Bawa tugas Structure dan alat tulis.") size 18 color "#67e8f9"


screen day_four_afternoon_choice():
    modal True
    zorder 110

    add Solid("#020617b8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        padding (54, 46)
        background Solid("#0b1f2eef")

        vbox:
            spacing 30

            vbox:
                xalign 0.5
                spacing 7
                text "HARI 4  •  14.15" xalign 0.5 size 19 bold True color "#67e8f9"
                text "Apa yang akan kamu lakukan?" xalign 0.5 size 42 bold True color "#f8fafc"
                text "Sesi Listening dimulai pukul 15.30 di Laboratorium Bahasa." xalign 0.5 size 21 color "#a9bdc9"

            hbox:
                xalign 0.5
                spacing 36

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#3d2027ee")
                    hover_background Solid("#7f1d2d")
                    action Return("skip")

                    vbox:
                        spacing 14
                        text "01" size 21 bold True color "#fda4af"
                        text "SKIP HARI INI" size 36 bold True color "#fff1f2"
                        add Solid("#fb7185") xsize 110 ysize 4
                        text "Kirim izin ke grup dan lewati sesi Listening." xsize 480 size 23 color "#fecdd3"
                        text "Latihan susulan akan ditambahkan." size 18 color "#fda4af"

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#123a42ee")
                    hover_background Solid("#0e7490")
                    action Return("prepare")

                    vbox:
                        spacing 14
                        text "02" size 21 bold True color "#67e8f9"
                        text "BERSIAP-SIAP" size 36 bold True color "#ecfeff"
                        add Solid("#22d3ee") xsize 110 ysize 4
                        text "Berangkat ke Laboratorium Bahasa dan berlatih Listening." xsize 480 size 23 color "#cffafe"
                        text "Bawa earphone dan catatan Reading." size 18 color "#67e8f9"


screen day_five_afternoon_choice():
    modal True
    zorder 110

    add Solid("#020617b8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        padding (54, 46)
        background Solid("#0b1f2eef")

        vbox:
            spacing 30

            vbox:
                xalign 0.5
                spacing 7
                text "HARI 5  •  14.05" xalign 0.5 size 19 bold True color "#67e8f9"
                text "Apa yang akan kamu lakukan?" xalign 0.5 size 42 bold True color "#f8fafc"
                text "Structure Lanjutan dimulai pukul 15.30 di perpustakaan." xalign 0.5 size 21 color "#a9bdc9"

            hbox:
                xalign 0.5
                spacing 36

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#3d2027ee")
                    hover_background Solid("#7f1d2d")
                    action Return("skip")

                    vbox:
                        spacing 14
                        text "01" size 21 bold True color "#fda4af"
                        text "SKIP HARI INI" size 36 bold True color "#fff1f2"
                        add Solid("#fb7185") xsize 110 ysize 4
                        text "Kirim izin ke grup dan lewati Structure Lanjutan." xsize 480 size 23 color "#fecdd3"
                        text "Latihan susulan akan ditambahkan." size 18 color "#fda4af"

                button:
                    xsize 570
                    ysize 270
                    padding (34, 30)
                    background Solid("#123a42ee")
                    hover_background Solid("#0e7490")
                    action Return("prepare")

                    vbox:
                        spacing 14
                        text "02" size 21 bold True color "#67e8f9"
                        text "BERSIAP-SIAP" size 36 bold True color "#ecfeff"
                        add Solid("#22d3ee") xsize 110 ysize 4
                        text "Berangkat dan belajar parallel serta reduced clauses." xsize 480 size 23 color "#cffafe"
                        text "Bawa catatan Structure dasar dan alat tulis." size 18 color "#67e8f9"


screen vocabulary_lesson_board(section="concept"):
    zorder 20

    frame at vocabulary_board_enter:
        xalign 0.5
        ypos 60
        xsize 1200
        ysize 660
        padding (14, 14)
        background Solid("#704522")

        frame:
            xfill True
            yfill True
            padding (48, 32)
            background Solid("#123b32f5")

            vbox:
                spacing 12

                fixed:
                    xfill True
                    ysize 42

                    text "HARI 1  •  VOCABULARY":
                        xpos 0
                        yalign 0.5
                        size 25
                        bold True
                        color "#fde68a"

                    text "TOEFL STUDY BOARD":
                        xalign 1.0
                        yalign 0.5
                        size 20
                        color "#a7f3d0"

                add Solid("#d6b875", xsize=1076, ysize=3)
                null height 5

                if section == "concept":
                    text "VOCABULARY IN CONTEXT" at vocabulary_chalk_appear(0.08):
                        size 43
                        bold True
                        color "#f8fafc"

                    text "Cari arti kata sesuai penggunaannya" at vocabulary_chalk_appear(0.28):
                        size 34
                        color "#ecfdf5"

                    text "dalam kalimat atau paragraf." at vocabulary_chalk_appear(0.48):
                        size 34
                        color "#ecfdf5"

                    null height 8
                    text "Konteks lebih penting daripada menebak arti pertama di kamus." at vocabulary_chalk_appear(0.72):
                        xsize 1080
                        size 28
                        color "#bfdbfe"

                elif section == "steps":
                    text "4 LANGKAH MENEMUKAN MAKNA" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "1. Baca kalimat dan konteks di sekitarnya." at vocabulary_chalk_appear(0.25) size 30 color "#ecfdf5"
                    text "2. Tandai kata atau hubungan yang menjadi petunjuk." at vocabulary_chalk_appear(0.43) size 30 color "#ecfdf5"
                    text "3. Prediksi makna sebelum melihat pilihan." at vocabulary_chalk_appear(0.61) size 30 color "#ecfdf5"
                    text "4. Parafrasekan dengan jawaban, lalu baca ulang." at vocabulary_chalk_appear(0.79) size 30 color "#ecfdf5"

                elif section == "clues":
                    text "PETUNJUK KONTEKS & BENTUK KATA" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "• Definisi: or, means, in other words" at vocabulary_chalk_appear(0.24) size 29 color "#ecfdf5"
                    text "• Contoh: such as, for example, including" at vocabulary_chalk_appear(0.40) size 29 color "#ecfdf5"
                    text "• Kontras: but, unlike, however, although" at vocabulary_chalk_appear(0.56) size 29 color "#ecfdf5"
                    text "• Sebab/hasil: because, so, therefore" at vocabulary_chalk_appear(0.72) size 29 color "#ecfdf5"
                    text "• Bentuk kata (tambahan): un-, re-, mis-, -less" at vocabulary_chalk_appear(0.88) size 29 color "#fde68a"

                elif section == "example":
                    text "CONTOH BERSAMA" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "Unlike his outgoing sister, Arman is reserved" at vocabulary_chalk_appear(0.25) size 29 color "#ecfdf5"
                    text "and rarely speaks in class." at vocabulary_chalk_appear(0.40) size 29 color "#ecfdf5"
                    null height 4
                    text "Unlike  →  menunjukkan kontras" at vocabulary_chalk_appear(0.58) size 29 color "#bfdbfe"
                    text "rarely speaks  →  memberi penjelasan" at vocabulary_chalk_appear(0.74) size 29 color "#bfdbfe"
                    text "reserved = quiet / pendiam" at vocabulary_chalk_appear(0.94) size 34 bold True color "#fde68a"

                else:
                    text "SEBELUM MENJAWAB" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "✓ Maknanya didukung oleh konteks?" at vocabulary_chalk_appear(0.28) size 31 color "#ecfdf5"
                    text "✓ Jenis katanya sesuai?" at vocabulary_chalk_appear(0.48) size 31 color "#ecfdf5"
                    text "✓ Kalimat hasil parafrasanya tetap masuk akal?" at vocabulary_chalk_appear(0.68) size 31 color "#ecfdf5"
                    null height 8
                    text "BACA  →  CARI PETUNJUK  →  UJI MAKNA" at vocabulary_chalk_appear(0.90) size 33 bold True color "#fde68a"


screen structure_lesson_board(section="core"):
    zorder 20

    frame at vocabulary_board_enter:
        xalign 0.5
        ypos 60
        xsize 1200
        ysize 660
        padding (14, 14)
        background Solid("#704522")

        frame:
            xfill True
            yfill True
            padding (48, 32)
            background Solid("#123b32f5")

            vbox:
                spacing 12

                fixed:
                    xfill True
                    ysize 42

                    text "HARI 2  •  STRUCTURE":
                        xpos 0
                        yalign 0.5
                        size 25
                        bold True
                        color "#fde68a"

                    text "TOEFL STUDY BOARD":
                        xalign 1.0
                        yalign 0.5
                        size 20
                        color "#a7f3d0"

                add Solid("#d6b875", xsize=1076, ysize=3)
                null height 5

                if section == "core":
                    text "INTI KALIMAT" at vocabulary_chalk_appear(0.08):
                        size 43
                        bold True
                        color "#f8fafc"

                    text "SUBJECT  +  FINITE VERB" at vocabulary_chalk_appear(0.28):
                        size 42
                        bold True
                        color "#fde68a"

                    text "The students study every morning." at vocabulary_chalk_appear(0.48):
                        size 32
                        color "#ecfdf5"

                    text "Subject: the students    •    Verb: study" at vocabulary_chalk_appear(0.70):
                        size 29
                        color "#bfdbfe"

                    text "Kalimat lengkap membutuhkan pasangan utama yang jelas." at vocabulary_chalk_appear(0.90):
                        xsize 1080
                        size 27
                        color "#a7f3d0"

                elif section == "main_pair":
                    text "TEMUKAN PASANGAN UTAMA" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "The books on the table belong to Rina." at vocabulary_chalk_appear(0.26) size 32 color "#ecfdf5"
                    null height 4
                    text "Subject  →  the books" at vocabulary_chalk_appear(0.46) size 31 color "#fde68a"
                    text "Verb       →  belong" at vocabulary_chalk_appear(0.62) size 31 color "#fde68a"
                    text "on the table  →  frasa tambahan, bukan subject" at vocabulary_chalk_appear(0.80) size 29 color "#bfdbfe"
                    text "Jangan tertipu kata benda yang paling dekat dengan verb." at vocabulary_chalk_appear(0.98) size 27 color "#a7f3d0"

                elif section == "finite":
                    text "FINITE VERB" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "students review  •  she reviews  •  they reviewed" at vocabulary_chalk_appear(0.25) size 29 color "#ecfdf5"
                    text "she is reviewing  •  they have reviewed" at vocabulary_chalk_appear(0.42) size 29 color "#ecfdf5"
                    null height 4
                    text "The students reviewing their notes.  ✗" at vocabulary_chalk_appear(0.63) size 29 color "#fca5a5"
                    text "The students are reviewing their notes.  ✓" at vocabulary_chalk_appear(0.80) size 29 color "#a7f3d0"
                    text "Bentuk -ing atau to + verb tidak dapat berdiri sendiri." at vocabulary_chalk_appear(0.98) size 27 color "#fde68a"

                elif section == "agreement":
                    text "SUBJECT–VERB AGREEMENT" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "The student studies every day." at vocabulary_chalk_appear(0.28) size 32 color "#ecfdf5"
                    text "The students study every day." at vocabulary_chalk_appear(0.47) size 32 color "#ecfdf5"
                    null height 5
                    text "Simple present, he/she/it  →  verb + s/es" at vocabulary_chalk_appear(0.67) size 29 color "#fde68a"
                    text "Plural subject     →  base verb" at vocabulary_chalk_appear(0.84) size 30 color "#fde68a"
                    text "Every participant needs a pencil." at vocabulary_chalk_appear(1.02) size 28 color "#bfdbfe"

                elif section == "clauses":
                    text "DEPENDENT + INDEPENDENT CLAUSE" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "Because the room was noisy," at vocabulary_chalk_appear(0.27) size 32 color "#bfdbfe"
                    text "the group moved to the library." at vocabulary_chalk_appear(0.45) size 32 color "#ecfdf5"
                    null height 5
                    text "Because ... noisy  →  dependent clause" at vocabulary_chalk_appear(0.66) size 29 color "#fde68a"
                    text "the group moved ...  →  independent clause" at vocabulary_chalk_appear(0.83) size 29 color "#fde68a"
                    text "Klausa utama tetap memerlukan subject + finite verb." at vocabulary_chalk_appear(1.01) size 27 color "#a7f3d0"

                elif section == "relative":
                    text "RELATIVE CLAUSE" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "The professor who teaches linguistics" at vocabulary_chalk_appear(0.24) size 31 color "#ecfdf5"
                    text "explains the rule clearly." at vocabulary_chalk_appear(0.40) size 31 color "#ecfdf5"
                    null height 4
                    text "who teaches linguistics  →  relative clause" at vocabulary_chalk_appear(0.61) size 28 color "#bfdbfe"
                    text "Main subject  →  professor" at vocabulary_chalk_appear(0.78) size 29 color "#fde68a"
                    text "Main verb      →  explains" at vocabulary_chalk_appear(0.94) size 29 color "#fde68a"

                else:
                    text "URUTAN MEMERIKSA SOAL" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "1. Tandai batas setiap klausa." at vocabulary_chalk_appear(0.25) size 30 color "#ecfdf5"
                    text "2. Cari subject dan finite verb utama." at vocabulary_chalk_appear(0.43) size 30 color "#ecfdf5"
                    text "3. Abaikan frasa tambahan untuk sementara." at vocabulary_chalk_appear(0.61) size 30 color "#ecfdf5"
                    text "4. Periksa singular/plural dan kelengkapan klausa." at vocabulary_chalk_appear(0.79) size 30 color "#ecfdf5"
                    null height 7
                    text "CLAUSE  →  SUBJECT  →  VERB  →  AGREEMENT" at vocabulary_chalk_appear(0.98) size 32 bold True color "#fde68a"


screen day_five_structure_lesson_board(section="parallel"):
    zorder 20

    frame at vocabulary_board_enter:
        xalign 0.5
        ypos 60
        xsize 1200
        ysize 660
        padding (14, 14)
        background Solid("#704522")

        frame:
            xfill True
            yfill True
            padding (48, 32)
            background Solid("#123b32f5")

            vbox:
                spacing 12

                fixed:
                    xfill True
                    ysize 42

                    text "HARI 5  •  STRUCTURE LANJUTAN":
                        xpos 0
                        yalign 0.5
                        size 25
                        bold True
                        color "#fde68a"

                    text "TOEFL STUDY BOARD":
                        xalign 1.0
                        yalign 0.5
                        size 20
                        color "#a7f3d0"

                add Solid("#d6b875", xsize=1076, ysize=3)
                null height 5

                if section == "parallel":
                    text "PARALLEL STRUCTURE" at vocabulary_chalk_appear(0.08):
                        size 42
                        bold True
                        color "#f8fafc"

                    text "Unsur dengan fungsi sama memakai bentuk yang sama." at vocabulary_chalk_appear(0.27):
                        size 29
                        color "#ecfdf5"

                    text "She enjoys reading, taking notes, and discussing ideas." at vocabulary_chalk_appear(0.48):
                        size 30
                        color "#a7f3d0"
                        substitute False

                    text "reading  •  taking notes  •  discussing ideas" at vocabulary_chalk_appear(0.68):
                        size 30
                        bold True
                        color "#fde68a"
                        substitute False

                    text "FORM SAMA  +  FUNCTION SAMA" at vocabulary_chalk_appear(0.90) size 31 bold True color "#bfdbfe"

                elif section == "paired":
                    text "PAIRED CONJUNCTIONS" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "both ... and     •     either ... or" at vocabulary_chalk_appear(0.25) size 31 color "#fde68a" substitute False
                    text "neither ... nor     •     not only ... but also" at vocabulary_chalk_appear(0.43) size 29 color "#fde68a" substitute False
                    null height 4
                    text "The study guide is both easy to use" at vocabulary_chalk_appear(0.61) size 30 color "#ecfdf5" substitute False
                    text "and simple to understand." at vocabulary_chalk_appear(0.75) size 30 color "#ecfdf5" substitute False
                    text "easy to use  =  adjective phrase" at vocabulary_chalk_appear(0.88) size 27 color "#a7f3d0" substitute False
                    text "simple to understand  =  adjective phrase" at vocabulary_chalk_appear(1.01) size 27 color "#a7f3d0" substitute False

                elif section == "relative_active":
                    text "REDUCED CLAUSE  •  ACTIVE" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "The students who are waiting outside ..." at vocabulary_chalk_appear(0.26) size 30 color "#ecfdf5" substitute False
                    text "The students waiting outside ..." at vocabulary_chalk_appear(0.45) size 30 color "#a7f3d0" substitute False
                    null height 4
                    text "who are waiting  →  waiting" at vocabulary_chalk_appear(0.66) size 33 bold True color "#fde68a" substitute False
                    text "Makna aktif: noun melakukan tindakan." at vocabulary_chalk_appear(0.85) size 29 color "#bfdbfe"
                    text "ACTIVE REDUCTION  →  V-ING" at vocabulary_chalk_appear(1.02) size 31 bold True color "#f8fafc"

                elif section == "relative_passive":
                    text "REDUCED CLAUSE  •  PASSIVE" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "The articles that were written by Leo ..." at vocabulary_chalk_appear(0.26) size 30 color "#ecfdf5" substitute False
                    text "The articles written by Leo ..." at vocabulary_chalk_appear(0.45) size 30 color "#a7f3d0" substitute False
                    null height 4
                    text "that were written  →  written" at vocabulary_chalk_appear(0.66) size 31 bold True color "#fde68a" substitute False
                    text "Makna pasif: noun menerima tindakan." at vocabulary_chalk_appear(0.85) size 29 color "#bfdbfe"
                    text "PASSIVE REDUCTION  →  V3" at vocabulary_chalk_appear(1.02) size 31 bold True color "#f8fafc"

                elif section == "adverb":
                    text "REDUCED ADVERB CLAUSE" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "While Rina was walking to class, she reviewed notes." at vocabulary_chalk_appear(0.25) size 28 color "#ecfdf5" substitute False
                    text "While walking to class, Rina reviewed her notes." at vocabulary_chalk_appear(0.44) size 29 color "#a7f3d0" substitute False
                    null height 4
                    text "Subject kedua klausa harus sama: Rina = Rina" at vocabulary_chalk_appear(0.65) size 29 bold True color "#fde68a" substitute False
                    text "While walking to class, the rain began.  ✗" at vocabulary_chalk_appear(0.83) size 28 color "#fca5a5" substitute False
                    text "CHECK SUBJECT  →  REDUCE" at vocabulary_chalk_appear(1.01) size 31 bold True color "#bfdbfe"

                elif section == "checklist":
                    text "CHECKLIST STRUCTURE LANJUTAN" at vocabulary_chalk_appear(0.08):
                        size 38
                        bold True
                        color "#f8fafc"

                    text "1. Apakah fungsi unsur-unsurnya sama?" at vocabulary_chalk_appear(0.24) size 29 color "#ecfdf5"
                    text "2. Apakah bentuk di kedua sisi conjunction setara?" at vocabulary_chalk_appear(0.41) size 28 color "#ecfdf5"
                    text "3. Apakah noun melakukan atau menerima tindakan?" at vocabulary_chalk_appear(0.58) size 28 color "#ecfdf5"
                    text "4. Apakah subject adverb clause dan main clause sama?" at vocabulary_chalk_appear(0.75) size 28 color "#ecfdf5"
                    null height 4
                    text "FORM  →  FUNCTION  →  VOICE  →  CHECK" at vocabulary_chalk_appear(0.98) size 31 bold True color "#fde68a"


screen reading_lesson_board(section="overview"):
    zorder 20

    frame at vocabulary_board_enter:
        xalign 0.5
        ypos 60
        xsize 1200
        ysize 660
        padding (14, 14)
        background Solid("#704522")

        frame:
            xfill True
            yfill True
            padding (48, 32)
            background Solid("#123b32f5")

            vbox:
                spacing 12

                fixed:
                    xfill True
                    ysize 42

                    text "HARI 3  •  READING":
                        xpos 0
                        yalign 0.5
                        size 25
                        bold True
                        color "#fde68a"

                    text "TOEFL STUDY BOARD":
                        xalign 1.0
                        yalign 0.5
                        size 20
                        color "#a7f3d0"

                add Solid("#d6b875", xsize=1076, ysize=3)
                null height 5

                if section == "overview":
                    text "READ WITH A PURPOSE" at vocabulary_chalk_appear(0.08):
                        size 43
                        bold True
                        color "#f8fafc"

                    text "QUESTION  →  PASSAGE  →  EVIDENCE" at vocabulary_chalk_appear(0.30):
                        size 37
                        bold True
                        color "#fde68a"

                    null height 7
                    text "Pahami apa yang ditanyakan." at vocabulary_chalk_appear(0.52) size 31 color "#ecfdf5"
                    text "Temukan bagian teks yang relevan." at vocabulary_chalk_appear(0.70) size 31 color "#ecfdf5"
                    text "Pilih jawaban yang didukung bukti." at vocabulary_chalk_appear(0.88) size 31 color "#ecfdf5"

                elif section == "main_idea":
                    text "TOPIC vs MAIN IDEA" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "TOPIC  →  apa yang dibahas?" at vocabulary_chalk_appear(0.28) size 31 color "#bfdbfe"
                    text "MAIN IDEA  →  apa pesan utama tentang topic?" at vocabulary_chalk_appear(0.47) size 31 color "#fde68a"
                    null height 6
                    text "Topic: regular sleep" at vocabulary_chalk_appear(0.67) size 29 color "#ecfdf5"
                    text "Main idea: tidur teratur mendukung kesehatan dan konsentrasi" at vocabulary_chalk_appear(0.84) size 28 color "#a7f3d0"
                    text "Jawaban harus mewakili keseluruhan passage." at vocabulary_chalk_appear(1.02) size 27 color "#f8fafc"

                elif section == "details":
                    text "SUPPORTING DETAILS" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "1. Ambil keyword dari pertanyaan." at vocabulary_chalk_appear(0.27) size 30 color "#ecfdf5"
                    text "2. Scan passage untuk kata atau sinonimnya." at vocabulary_chalk_appear(0.45) size 30 color "#ecfdf5"
                    text "3. Baca satu kalimat sebelum dan sesudahnya." at vocabulary_chalk_appear(0.63) size 30 color "#ecfdf5"
                    null height 7
                    text "DETAIL = informasi yang dinyatakan langsung" at vocabulary_chalk_appear(0.83) size 31 bold True color "#fde68a"
                    text "Jangan mengganti bukti teks dengan ingatan pribadi." at vocabulary_chalk_appear(1.01) size 27 color "#bfdbfe"

                elif section == "reference_vocab":
                    text "REFERENCE & VOCABULARY" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "Pronoun reference:" at vocabulary_chalk_appear(0.26) size 29 bold True color "#fde68a"
                    text "Cari noun sebelumnya yang paling logis." at vocabulary_chalk_appear(0.42) size 29 color "#ecfdf5"
                    null height 4
                    text "Vocabulary in context:" at vocabulary_chalk_appear(0.62) size 29 bold True color "#fde68a"
                    text "Ganti kata target dengan pilihan, lalu baca ulang." at vocabulary_chalk_appear(0.79) size 29 color "#ecfdf5"
                    text "Makna harus cocok dengan kalimat dan paragraf." at vocabulary_chalk_appear(0.97) size 28 color "#bfdbfe"

                elif section == "inference":
                    text "INFERENCE" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "Tidak tertulis persis, tetapi didukung teks." at vocabulary_chalk_appear(0.29) size 31 color "#ecfdf5"
                    null height 5
                    text "EVIDENCE  +  LOGIC  =  INFERENCE" at vocabulary_chalk_appear(0.50) size 36 bold True color "#fde68a"
                    null height 5
                    text "✓ Kesimpulan paling aman" at vocabulary_chalk_appear(0.72) size 30 color "#a7f3d0"
                    text "✗ Pendapat pribadi atau klaim terlalu jauh" at vocabulary_chalk_appear(0.90) size 30 color "#fca5a5"

                else:
                    text "URUTAN MENJAWAB READING" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "1. Kenali jenis pertanyaannya." at vocabulary_chalk_appear(0.25) size 30 color "#ecfdf5"
                    text "2. Temukan bukti dalam passage." at vocabulary_chalk_appear(0.43) size 30 color "#ecfdf5"
                    text "3. Coret pilihan yang bertentangan atau terlalu luas." at vocabulary_chalk_appear(0.61) size 30 color "#ecfdf5"
                    text "4. Baca ulang jawaban bersama konteksnya." at vocabulary_chalk_appear(0.79) size 30 color "#ecfdf5"
                    null height 7
                    text "PREVIEW  →  QUESTION TYPE  →  EVIDENCE  →  ANSWER" at vocabulary_chalk_appear(0.98) size 29 bold True color "#fde68a"


screen listening_lesson_board(section="overview"):
    zorder 20

    frame at vocabulary_board_enter:
        xalign 0.5
        ypos 60
        xsize 1200
        ysize 660
        padding (14, 14)
        background Solid("#704522")

        frame:
            xfill True
            yfill True
            padding (48, 32)
            background Solid("#123b32f5")

            vbox:
                spacing 12

                fixed:
                    xfill True
                    ysize 42

                    text "HARI 4  •  LISTENING":
                        xpos 0
                        yalign 0.5
                        size 25
                        bold True
                        color "#fde68a"

                    text "TOEFL STUDY BOARD":
                        xalign 1.0
                        yalign 0.5
                        size 20
                        color "#a7f3d0"

                add Solid("#d6b875", xsize=1076, ysize=3)
                null height 5

                if section == "overview":
                    text "LISTEN WITH A PURPOSE" at vocabulary_chalk_appear(0.08):
                        size 43
                        bold True
                        color "#f8fafc"

                    text "QUESTION  →  KEYWORDS  →  INTENT" at vocabulary_chalk_appear(0.30):
                        size 37
                        bold True
                        color "#fde68a"

                    null height 7
                    text "Baca pertanyaan dan pilihan dengan cepat." at vocabulary_chalk_appear(0.52) size 31 color "#ecfdf5"
                    text "Dengarkan informasi yang menentukan jawaban." at vocabulary_chalk_appear(0.70) size 31 color "#ecfdf5"
                    text "Jangan berhenti hanya karena kehilangan satu kata." at vocabulary_chalk_appear(0.88) size 30 color "#bfdbfe"

                elif section == "main_idea":
                    text "TOPIC & MAIN IDEA" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "TOPIC  →  apa yang dibicarakan?" at vocabulary_chalk_appear(0.27) size 31 color "#bfdbfe"
                    text "MAIN IDEA  →  apa inti percakapannya?" at vocabulary_chalk_appear(0.45) size 31 color "#fde68a"
                    null height 6
                    text "Perhatikan masalah, respons, dan hasil pembicaraan." at vocabulary_chalk_appear(0.66) size 29 color "#ecfdf5"
                    text "Jawaban harus mencakup arah percakapan secara utuh." at vocabulary_chalk_appear(0.84) size 29 color "#a7f3d0"
                    text "Jangan memilih detail yang hanya disebut sekilas." at vocabulary_chalk_appear(1.02) size 27 color "#f8fafc"

                elif section == "detail":
                    text "LISTEN FOR DETAILS" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "WHO  •  WHERE  •  WHEN  •  NUMBER  •  ACTION" at vocabulary_chalk_appear(0.28) size 31 bold True color "#fde68a"
                    null height 5
                    text "1. Ambil keyword dari pertanyaan." at vocabulary_chalk_appear(0.48) size 30 color "#ecfdf5"
                    text "2. Dengarkan sinonim atau parafrasanya." at vocabulary_chalk_appear(0.65) size 30 color "#ecfdf5"
                    text "3. Catat singkat; jangan menulis seluruh kalimat." at vocabulary_chalk_appear(0.82) size 30 color "#ecfdf5"
                    text "Pilihan benar menyampaikan informasi yang sama." at vocabulary_chalk_appear(1.00) size 28 color "#bfdbfe"

                elif section == "intent_suggestion":
                    text "INTENT & SUGGESTION" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "Why don't you ...?  →  suggestion" at vocabulary_chalk_appear(0.27) size 31 color "#fde68a"
                    text "You could / You should ...  →  advice" at vocabulary_chalk_appear(0.45) size 31 color "#fde68a"
                    null height 5
                    text "Perhatikan tone dan respons pembicara kedua." at vocabulary_chalk_appear(0.66) size 29 color "#ecfdf5"
                    text "Maksud pembicara sering diparafrasakan di jawaban." at vocabulary_chalk_appear(0.84) size 29 color "#a7f3d0"
                    text "Kata yang sama persis belum tentu menjadi jawaban." at vocabulary_chalk_appear(1.02) size 27 color "#bfdbfe"

                elif section == "inference":
                    text "LISTENING INFERENCE" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "AUDIO EVIDENCE  +  CONTEXT  =  INFERENCE" at vocabulary_chalk_appear(0.30) size 34 bold True color "#fde68a"
                    null height 7
                    text "Gunakan apa yang dikatakan dan bagaimana responsnya." at vocabulary_chalk_appear(0.53) size 30 color "#ecfdf5"
                    text "✓ Kesimpulan paling aman dari percakapan" at vocabulary_chalk_appear(0.73) size 30 color "#a7f3d0"
                    text "✗ Asumsi pribadi atau kepastian yang tidak terdengar" at vocabulary_chalk_appear(0.91) size 29 color "#fca5a5"

                elif section == "checklist":
                    text "URUTAN MENJAWAB LISTENING" at vocabulary_chalk_appear(0.08):
                        size 40
                        bold True
                        color "#f8fafc"

                    text "1. Preview pertanyaan dan pilihan." at vocabulary_chalk_appear(0.24) size 30 color "#ecfdf5"
                    text "2. Tangkap keyword, contrast, dan suggestion." at vocabulary_chalk_appear(0.41) size 30 color "#ecfdf5"
                    text "3. Tentukan intent atau next action." at vocabulary_chalk_appear(0.58) size 30 color "#ecfdf5"
                    text "4. Pilih parafrasa yang paling didukung audio." at vocabulary_chalk_appear(0.75) size 30 color "#ecfdf5"
                    null height 7
                    text "PREVIEW  →  LISTEN  →  INTENT  →  ANSWER" at vocabulary_chalk_appear(0.96) size 31 bold True color "#fde68a"

                else:
                    text "LISTENING HARI 4" size 42 bold True color "#f8fafc"
                    text "Gunakan section materi yang tersedia." size 30 color "#bfdbfe"


screen day_one_speaker_portrait(speaker):
    zorder 21

    $ portrait_path, speaker_label, speaker_role, accent_color = day_one_speaker_portrait_data(speaker)

    frame at lesson_speaker_card_enter:
        xpos 1580
        ypos 100
        xsize 300
        ysize 620
        padding (10, 10)
        background Solid("#07131ff2")

        fixed:
            xsize 280
            ysize 600

            add Solid(accent_color) xpos 0 ypos 0 xsize 280 ysize 5
            add Transform(portrait_path, crop=(0, 0, 1024, 1280), xysize=(280, 350)) xpos 0 ypos 10

            frame:
                xpos 0
                ypos 365
                xsize 280
                ysize 185
                padding (18, 18)
                background Solid("#0b1f2ef5")

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 8

                    text speaker_role:
                        xalign 0.5
                        size 17
                        bold True
                        color accent_color

                    text speaker_label:
                        xalign 0.5
                        text_align 0.5
                        xsize 244
                        size (24 if speaker == "player" else 31)
                        bold True
                        color "#f8fafc"

                    text "SEDANG BERBICARA":
                        xalign 0.5
                        size 15
                        color "#94a3b8"


screen study_desk_inventory(title_text="PERSIAPAN PAGI  •  MEJA BELAJAR"):
    modal True
    zorder 120
    default picked = []
    default hovered_item = None

    $ item_labels = {
        "notebook": "Buku catatan",
        "pencil": "Pensil",
        "eraser": "Penghapus",
        "phone": "Ponsel",
        "id_card": "Kartu identitas",
        "water": "Botol minum",
        "earphone": "Earphone",
    }
    $ item_images = {
        "notebook": "day7 item notebook",
        "pencil": "day7 item pencil",
        "eraser": "day7 item eraser",
        "phone": "day7 item phone",
        "id_card": "day7 item id_card",
        "water": "day7 item water",
        "earphone": "day7 item earphone",
    }

    add "bg day7 study desk"
    add Solid("#02061788")

    frame:
        xalign 0.5
        yalign 0.08
        xsize 1180
        padding (34, 24)
        background Solid("#071923ee")

        vbox:
            spacing 10
            text title_text xalign 0.5 size 31 bold True color "#67e8f9"
            text "Klik gambar barang untuk memilih atau membatalkan pilihan. Tidak ada barang wajib." xalign 0.5 text_align 0.5 size 20 color "#dbeafe"

    # Hotspot visual barang di atas meja. Hover memperbesar dan menerangi objek.
    for item_name, item_pos in [("notebook", (690, 675)), ("pencil", (940, 645)), ("eraser", (1200, 770)), ("phone", (1450, 660)), ("id_card", (400, 720)), ("water", (530, 565)), ("earphone", (1190, 620))]:
        button:
            xpos item_pos[0]
            ypos item_pos[1]
            xsize 220
            ysize 220
            padding (0, 0)
            background None
            hover_background None
            action SetScreenVariable("picked", toggle_inventory_item(picked, item_name))
            hovered SetScreenVariable("hovered_item", item_name)
            unhovered SetScreenVariable("hovered_item", None)
            if hovered_item == item_name:
                add Transform(item_images[item_name], xysize=(205, 205), matrixcolor=BrightnessMatrix(0.35)) xalign 0.5 yalign 0.45
            else:
                add Transform(item_images[item_name], xysize=(185, 185)) xalign 0.5 yalign 0.45
            text ("✓ " if item_name in picked else "") + item_labels[item_name]:
                xalign 0.5
                yalign 0.98
                text_align 0.5
                size 16
                bold True
                color "#f8fafc"

    frame:
        xalign 0.86
        yalign 0.58
        xsize 480
        ysize 360
        padding (26, 22)
        background Solid("#071923ee")

        vbox:
            spacing 12
            text "ISI TAS" size 25 bold True color "#fde68a"
            text "[len(picked)] barang dipilih" size 20 color "#cbd5e1"
            for item_name in ["notebook", "pencil", "eraser", "phone", "id_card", "water", "earphone"]:
                text ("✓ " if item_name in picked else "□ ") + item_labels[item_name]:
                    size 19
                    color ("#a7f3d0" if item_name in picked else "#94a3b8")
            null height 6
            text "Tidak ada barang wajib. Kamu bebas membawa atau meninggalkan item apa pun." size 16 color "#fbbf24" line_spacing 3
            textbutton "MASUKKAN KE TAS  →":
                xfill True
                ysize 62
                background Solid("#0e7490")
                hover_background Solid("#0891b2")
                insensitive_background Solid("#334155")
                text_color "#ffffff"
                text_insensitive_color "#94a3b8"
                text_size 21
                action Return(picked)


screen study_hint_panel(previous_score, hint_text):
    default hint_visible = False
    $ hint_level = study_hint_level(previous_score)
    if day == 7 and hint_level > 0:
        hbox:
            xfill True
            spacing 12
            textbutton ("TUTUP HINT" if hint_visible else "BUKA HINT • LEVEL [hint_level]"):
                xsize 260
                ysize 48
                background Solid("#164e63")
                hover_background Solid("#0e7490")
                text_color "#cffafe"
                text_size 17
                action SetScreenVariable("hint_visible", not hint_visible)
            text "Hint memakai skor akumulasi hari sebelumnya: [previous_score] poin." yalign 0.5 size 17 color "#94a3b8"
        if hint_visible:
            frame:
                xfill True
                padding (18, 12)
                background Solid("#123a42")
                vbox:
                    spacing 4
                    text "TERJEMAHAN KONTEKS & MATERI" size 16 bold True color "#fde68a"
                    text hint_text size 19 color "#ecfeff" line_spacing 3 substitute False
    elif day == 7:
        text "HINT TERKUNCI • Raih minimal 30 poin dari hari sebelumnya untuk membukanya." size 16 color "#94a3b8"


screen extra_study_quiz(day_number, skill_label, prompt, option_a, option_b, option_c, previous_score, hint_text=None):
    modal True
    zorder 115
    default hint_visible = False
    $ hint_level = study_hint_level(previous_score)

    add Solid("#020617e8")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1180
        padding (42, 34)
        background Solid("#0b1f2ef7")
        vbox:
            spacing 18
            text "LATIHAN BONUS • HARI [day_number] • [skill_label]" xalign 0.5 size 27 bold True color "#fbbf24"
            text "Soal tambahan • +10 poin bonus" xalign 0.5 size 18 color "#fde68a"
            text prompt xsize 1090 size 29 bold True color "#f8fafc" line_spacing 5 substitute False
            add Solid("#1e5363") xsize 1090 ysize 2
            if day == 7 and hint_level > 0:
                textbutton ("TUTUP HINT" if hint_visible else "BUKA HINT • LEVEL [hint_level]"):
                    xalign 1.0
                    xsize 280
                    ysize 48
                    background Solid("#164e63")
                    hover_background Solid("#0e7490")
                    text_color "#cffafe"
                    text_size 17
                    action SetScreenVariable("hint_visible", not hint_visible)
                if hint_visible:
                    frame:
                        xfill True
                        padding (18, 12)
                        background Solid("#123a42")
                        text (hint_text or study_hint_for("mixed")) xsize 1050 size 19 color "#ecfeff" substitute False
            elif day == 7:
                text "HINT TERKUNCI • Raih minimal 30 poin dari hari sebelumnya." size 16 color "#94a3b8"
            for option, label in [("a", option_a), ("b", option_b), ("c", option_c)]:
                button:
                    xfill True
                    ysize 72
                    padding (22, 12)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    action Return(option)
                    text (option.upper() + ".  " + label) xsize 1030 yalign 0.5 size 23 color "#ecfeff" substitute False


screen day_one_vocab_quiz(question_number, prompt, option_a, option_b, option_c, hint_text=None):
    modal True
    zorder 110

    add Solid("#020617c9")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        padding (48, 40)
        background Solid("#0b1f2ef5")

        vbox:
            spacing 22

            fixed:
                xsize 1020
                ysize 30

                text "LATIHAN VOCABULARY  •  SOAL [question_number]/5" size 19 bold True color "#67e8f9"
                text "SKOR  [day_1_vocab_score]/50  •  +10 JIKA BENAR" xalign 1.0 size 19 bold True color "#fde68a"

            text prompt xsize 1020 size 32 bold True color "#f8fafc" line_spacing 5
            add Solid("#1e5363") xsize 1020 ysize 2
            use study_hint_panel(0, hint_text or study_hint_for("vocabulary"))

            textbutton "A.  [option_a]":
                xfill True
                ysize 76
                padding (24, 16)
                background Solid("#123a42")
                hover_background Solid("#0e7490")
                text_color "#ecfeff"
                text_size 25
                action Return("a")

            textbutton "B.  [option_b]":
                xfill True
                ysize 76
                padding (24, 16)
                background Solid("#123a42")
                hover_background Solid("#0e7490")
                text_color "#ecfeff"
                text_size 25
                action Return("b")

            textbutton "C.  [option_c]":
                xfill True
                ysize 76
                padding (24, 16)
                background Solid("#123a42")
                hover_background Solid("#0e7490")
                text_color "#ecfeff"
                text_size 25
                action Return("c")


screen day_two_structure_quiz(question_number, prompt, option_a, option_b, option_c, hint_text=None):
    modal True
    zorder 110

    add Solid("#020617c9")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        padding (48, 40)
        background Solid("#0b1f2ef5")

        vbox:
            spacing 22

            fixed:
                xsize 1020
                ysize 30

                text "LATIHAN STRUCTURE  •  SOAL [question_number]/5" size 19 bold True color "#67e8f9"
                text "SKOR  [day_2_structure_score]/50  •  +10 JIKA BENAR" xalign 1.0 size 19 bold True color "#fde68a"

            text prompt xsize 1020 size 32 bold True color "#f8fafc" line_spacing 5
            add Solid("#1e5363") xsize 1020 ysize 2
            use study_hint_panel(day_1_vocab_score + extra_practice_score, hint_text or study_hint_for("structure"))

            textbutton "A.  [option_a]":
                xfill True
                ysize 76
                padding (24, 16)
                background Solid("#123a42")
                hover_background Solid("#0e7490")
                text_color "#ecfeff"
                text_size 25
                action Return("a")

            textbutton "B.  [option_b]":
                xfill True
                ysize 76
                padding (24, 16)
                background Solid("#123a42")
                hover_background Solid("#0e7490")
                text_color "#ecfeff"
                text_size 25
                action Return("b")

            textbutton "C.  [option_c]":
                xfill True
                ysize 76
                padding (24, 16)
                background Solid("#123a42")
                hover_background Solid("#0e7490")
                text_color "#ecfeff"
                text_size 25
                action Return("c")


screen day_five_structure_quiz(question_number, prompt, option_a, option_b, option_c, hint_text=None):
    modal True
    zorder 110

    add Solid("#020617c9")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1240
        padding (48, 40)
        background Solid("#0b1f2ef5")

        vbox:
            spacing 22

            fixed:
                xsize 1140
                ysize 30

                text "STRUCTURE LANJUTAN  •  SOAL [question_number]/5" size 19 bold True color "#67e8f9"
                text "SKOR  [day_5_structure_score]/50  •  +10 JIKA BENAR" xalign 1.0 size 19 bold True color "#fde68a"

            text prompt:
                xsize 1140
                size 31
                bold True
                color "#f8fafc"
                line_spacing 5
                substitute False

            add Solid("#1e5363") xsize 1140 ysize 2
            use study_hint_panel(day_1_vocab_score + day_2_structure_score + day_3_reading_score + day_4_listening_score + extra_practice_score, hint_text or study_hint_for("structure"))

            button:
                xfill True
                ysize 88
                padding (24, 14)
                background Solid("#123a42")
                hover_background Solid("#0e7490")
                action Return("a")

                text ("A.  " + option_a):
                    xsize 1085
                    yalign 0.5
                    size 25
                    color "#ecfeff"
                    substitute False

            button:
                xfill True
                ysize 88
                padding (24, 14)
                background Solid("#123a42")
                hover_background Solid("#0e7490")
                action Return("b")

                text ("B.  " + option_b):
                    xsize 1085
                    yalign 0.5
                    size 25
                    color "#ecfeff"
                    substitute False

            button:
                xfill True
                ysize 88
                padding (24, 14)
                background Solid("#123a42")
                hover_background Solid("#0e7490")
                action Return("c")

                text ("C.  " + option_c):
                    xsize 1085
                    yalign 0.5
                    size 25
                    color "#ecfeff"
                    substitute False


screen day_three_reading_quiz(question_number, passage_title, passage, prompt, option_a, option_b, option_c, hint_text=None):
    modal True
    zorder 110

    add Solid("#020617d9")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1700
        ysize 900
        padding (40, 36)
        background Solid("#0b1f2ef5")

        vbox:
            spacing 20

            fixed:
                xsize 1620
                ysize 34

                text "LATIHAN READING  •  SOAL [question_number]/5" size 20 bold True color "#67e8f9"
                text "SKOR  [day_3_reading_score]/50  •  +10 JIKA BENAR" xalign 1.0 size 20 bold True color "#fde68a"

            hbox:
                spacing 30

                frame:
                    xsize 920
                    ysize 760
                    padding (34, 30)
                    background Solid("#102b35")

                    viewport:
                        xfill True
                        yfill True
                        mousewheel True
                        draggable True

                        vbox:
                            xsize 852
                            spacing 18

                            text passage_title:
                                size 22
                                bold True
                                color "#fde68a"
                                substitute False
                            add Solid("#2b6672") xsize 852 ysize 2
                            text passage:
                                xsize 852
                                size 26
                                color "#f8fafc"
                                line_spacing 7
                                substitute False

                            null height 8
                            text "Passage tetap tersedia selama semua soal." size 18 italic True color "#94a3b8"

                frame:
                    xsize 670
                    ysize 760
                    padding (30, 28)
                    background Solid("#071923")

                    vbox:
                        spacing 18

                        text "PERTANYAAN [question_number]" size 18 bold True color "#22d3ee"
                        text prompt:
                            xsize 610
                            size 29
                            bold True
                            color "#f8fafc"
                            line_spacing 5
                            substitute False

                        use study_hint_panel(day_1_vocab_score + day_2_structure_score + extra_practice_score, hint_text or study_hint_for("reading"))

                        add Solid("#1e5363") xsize 610 ysize 2

                        button:
                            xfill True
                            ysize 132
                            padding (22, 16)
                            background Solid("#123a42")
                            hover_background Solid("#0e7490")
                            action Return("a")

                            text ("A.  " + option_a):
                                xsize 566
                                yalign 0.5
                                size 22
                                color "#ecfeff"
                                substitute False

                        button:
                            xfill True
                            ysize 132
                            padding (22, 16)
                            background Solid("#123a42")
                            hover_background Solid("#0e7490")
                            action Return("b")

                            text ("B.  " + option_b):
                                xsize 566
                                yalign 0.5
                                size 22
                                color "#ecfeff"
                                substitute False

                        button:
                            xfill True
                            ysize 132
                            padding (22, 16)
                            background Solid("#123a42")
                            hover_background Solid("#0e7490")
                            action Return("c")

                            text ("C.  " + option_c):
                                xsize 566
                                yalign 0.5
                                size 22
                                color "#ecfeff"
                                substitute False


screen day_four_listening_quiz(question_number, audio_file, prompt, option_a, option_b, option_c, hint_text=None):
    modal True
    zorder 110
    default replay_count = 0
    default audio_started = False

    $ audio_finished = audio_started and not renpy.music.is_playing(channel="listening")

    on "show" action [
        Stop("listening"),
        Play("listening", audio_file, loop=False),
        SetScreenVariable("audio_started", True),
    ]
    on "hide" action Stop("listening")
    on "replaced" action Stop("listening")
    key "game_menu" action NullAction()

    timer 0.10 repeat True action Function(renpy.restart_interaction)

    add Solid("#020617e6")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1700
        ysize 900
        padding (40, 36)
        background Solid("#0b1f2ef7")

        vbox:
            spacing 20

            fixed:
                xsize 1620
                ysize 34

                text "LATIHAN LISTENING  •  SOAL [question_number]/5" size 20 bold True color "#67e8f9"
                text "SKOR  [day_4_listening_score]/50  •  +10 JIKA BENAR" xalign 1.0 size 20 bold True color "#fde68a"

            hbox:
                spacing 30

                frame:
                    xsize 570
                    ysize 760
                    padding (34, 32)
                    background Solid("#102b35")

                    vbox:
                        xfill True
                        spacing 22

                        text "AUDIO PLAYER" xalign 0.5 size 22 bold True color "#fde68a"
                        add Solid("#2b6672") xsize 502 ysize 2

                        null height 30

                        frame:
                            xalign 0.5
                            xsize 190
                            ysize 190
                            padding (0, 0)
                            background Solid("#0e7490")

                            text "♫":
                                xalign 0.5
                                yalign 0.5
                                size 92
                                bold True
                                color "#ecfeff"

                        if not audio_finished:
                            text "AUDIO SEDANG DIPUTAR":
                                xalign 0.5
                                size 24
                                bold True
                                color "#67e8f9"
                        elif replay_count == 0:
                            text "AUDIO SELESAI  •  REPLAY TERSEDIA":
                                xalign 0.5
                                text_align 0.5
                                size 22
                                bold True
                                color "#a7f3d0"
                        else:
                            text "AUDIO SELESAI  •  REPLAY TERPAKAI":
                                xalign 0.5
                                text_align 0.5
                                size 22
                                bold True
                                color "#f8fafc"

                        bar:
                            value AudioPositionValue(channel="listening", update_interval=0.05)
                            xfill True
                            ysize 16
                            left_bar Solid("#22d3ee")
                            right_bar Solid("#334155")

                        textbutton "PUTAR ULANG  •  MAKS. 1×":
                            xalign 0.5
                            xsize 410
                            ysize 72
                            padding (22, 14)
                            background Solid("#164e63")
                            hover_background Solid("#0e7490")
                            insensitive_background Solid("#1e293b")
                            text_color "#ecfeff"
                            text_insensitive_color "#64748b"
                            text_size 22
                            sensitive audio_finished and replay_count < 1
                            action [
                                SetScreenVariable("audio_started", False),
                                SetScreenVariable("replay_count", replay_count + 1),
                                Play("listening", audio_file, loop=False),
                                SetScreenVariable("audio_started", True),
                            ]

                        text "Pilihan jawaban terbuka setelah audio selesai. Transcript ditampilkan sesudah kamu menjawab.":
                            xalign 0.5
                            text_align 0.5
                            xsize 480
                            size 19
                            color "#94a3b8"

                frame:
                    xsize 1020
                    ysize 760
                    padding (34, 30)
                    background Solid("#071923")

                    vbox:
                        spacing 18

                        text "PERTANYAAN [question_number]" size 18 bold True color "#22d3ee"
                        text prompt:
                            xsize 952
                            size 31
                            bold True
                            color "#f8fafc"
                            line_spacing 5
                            substitute False

                        use study_hint_panel(day_1_vocab_score + day_2_structure_score + day_3_reading_score + extra_practice_score, hint_text or study_hint_for("listening"))

                        add Solid("#1e5363") xsize 952 ysize 2

                        button:
                            xfill True
                            ysize 132
                            padding (24, 17)
                            background Solid("#123a42")
                            hover_background Solid("#0e7490")
                            insensitive_background Solid("#17252d")
                            sensitive audio_finished
                            action [Stop("listening"), Return("a")]

                            text ("A.  " + option_a):
                                xsize 900
                                yalign 0.5
                                size 24
                                color ("#ecfeff" if audio_finished else "#64748b")
                                substitute False

                        button:
                            xfill True
                            ysize 132
                            padding (24, 17)
                            background Solid("#123a42")
                            hover_background Solid("#0e7490")
                            insensitive_background Solid("#17252d")
                            sensitive audio_finished
                            action [Stop("listening"), Return("b")]

                            text ("B.  " + option_b):
                                xsize 900
                                yalign 0.5
                                size 24
                                color ("#ecfeff" if audio_finished else "#64748b")
                                substitute False

                        button:
                            xfill True
                            ysize 132
                            padding (24, 17)
                            background Solid("#123a42")
                            hover_background Solid("#0e7490")
                            insensitive_background Solid("#17252d")
                            sensitive audio_finished
                            action [Stop("listening"), Return("c")]

                            text ("C.  " + option_c):
                                xsize 900
                                yalign 0.5
                                size 24
                                color ("#ecfeff" if audio_finished else "#64748b")
                                substitute False

                        if not audio_finished:
                            text "Dengarkan sampai selesai untuk membuka pilihan.":
                                xalign 0.5
                                size 19
                                color "#fbbf24"


screen day_four_listening_transcript(question_number, transcript, evidence):
    modal True
    zorder 115

    on "show" action Stop("listening")
    on "hide" action Stop("listening")
    on "replaced" action Stop("listening")

    add Solid("#020617e6")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1500
        ysize 860
        padding (44, 38)
        background Solid("#0b1f2ef7")

        vbox:
            spacing 20

            fixed:
                xsize 1412
                ysize 42

                text "TRANSCRIPT & PEMBAHASAN  •  SOAL [question_number]/5" size 22 bold True color "#67e8f9"
                text "LISTENING HARI 4" xalign 1.0 size 20 bold True color "#fde68a"

            add Solid("#1e5363") xsize 1412 ysize 3

            frame:
                xfill True
                ysize 390
                padding (30, 26)
                background Solid("#102b35")

                viewport:
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True

                    vbox:
                        xsize 1352
                        spacing 14
                        text "TRANSCRIPT AUDIO" size 19 bold True color "#fde68a"
                        text transcript:
                            xsize 1352
                            size 28
                            color "#f8fafc"
                            line_spacing 7
                            substitute False

            frame:
                xfill True
                ysize 180
                padding (30, 24)
                background Solid("#123a42")

                vbox:
                    spacing 10
                    text "BUKTI KUNCI" size 19 bold True color "#67e8f9"
                    text evidence:
                        xsize 1352
                        size 27
                        color "#ecfeff"
                        line_spacing 5
                        substitute False

            textbutton "LANJUTKAN  →":
                xalign 1.0
                xsize 300
                ysize 68
                padding (24, 12)
                background Solid("#0e7490")
                hover_background Solid("#0891b2")
                text_color "#ffffff"
                text_size 23
                action [Stop("listening"), Return(True)]


screen whatsapp_day_one_skip_chat():
    modal True
    zorder 100
    default can_dismiss = False

    add Solid("#000000b8")

    fixed at screen_shake:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "07:18" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Anda",
                "Pagi, semuanya. Maaf, badanku kurang fit dan kepalaku pusing. Hari ini aku tidak bisa ikut. Tolong kirim catatannya; nanti akan kupelajari.",
                0, 535, 120, 0.25, "#128c7e", True
            )

            use whatsapp_group_text_message(
                "Rina",
                "Tidak apa-apa, [player_name]. Istirahat dulu. Nanti aku foto catatannya.",
                130, 500, 90, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Cepat sembuh. Jatah panik vocabulary-mu akan kami wakili dengan penuh tanggung jawab.",
                222, 520, 90, 1.85, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Koordinator party terkena debuff! Tenang, quest harian tetap lanjut!",
                322, 490, 90, 2.65, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Jangan memaksakan diri. Ringkasan dan soal latihannya akan kukirim setelah selesai.",
                414, 520, 90, 3.45, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Leo",
                "Kesehatan lebih penting. Istirahatlah. Setelah membaik, kerjakan latihan Vocabulary susulan yang kukirim.",
                514, 535, 110, 4.25, "#00897b"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.15 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_one_summary_notification():
    modal True
    zorder 130

    frame at whatsapp_notification_pop:
        xalign 0.5
        ypos 54
        xsize 760
        ysize 126
        padding (20, 14)
        background Solid("#101827f2")

        hbox:
            spacing 18

            fixed:
                xsize 82
                ysize 82
                add Solid("#128c7e")
                text "WA" xalign 0.5 yalign 0.5 size 27 bold True color "#ffffff"

            vbox:
                xsize 610
                spacing 3
                text "WHATSAPP  •  SEKARANG" size 16 bold True color "#76d8c9"
                text "Seven Days to TOEFL" size 25 bold True color "#ffffff"
                text "Leo: Ringkasan Vocabulary Hari 1 sudah kukirim." xsize 590 size 19 color "#d9e4e8"

    timer 1.60 action Return(True)


screen whatsapp_day_one_summary_chat():
    modal True
    zorder 120
    default choices_ready = False

    add Solid("#000000c7")

    fixed at screen_shake:
        xpos 100
        ypos 40
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:47" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Leo",
                "Ringkasan Maya sudah kuperiksa. Ini versi akhirnya.\n\nVOCABULARY HARI 1\n1. Baca konteks dan tandai petunjuk.\n2. Prediksi, parafrase, lalu periksa ulang.\nadjacent = bersebelahan | temporary = sementara\nambiguous = tidak jelas | nocturnal = aktif pada malam hari\nmisinterpret = menafsirkan secara keliru\nTugas: buat satu kalimat untuk setiap kata.",
                0, 560, 315, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Dua typo-ku gugur saat diperiksa Leo. Semoga pengorbanannya tidak sia-sia.",
                325, 520, 95, 1.15, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Aku paling memahami nocturnal. Akhirnya ada kosakata yang mewakili jalan hidupku.",
                430, 535, 100, 2.00, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Itu bukan pencapaian, Bima. Itu tanda kamu harus memperbaiki jam tidur.",
                540, 520, 100, 2.85, "#d94683"
            )

        if choices_ready:
            text "Pilih balasan di sebelah kanan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pesan baru sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    frame:
        xpos 900
        ypos 140
        xsize 880
        ysize 800
        padding (44, 44)
        background Solid("#0b1f2ef2")

        if choices_ready:
            vbox at whatsapp_message_fade(0.0):
                xfill True
                spacing 16

                text "PILIH BALASAN" size 20 bold True color "#22d3ee"
                text "Apa yang akan dikirim [player_name] ke grup?" xsize 792 size 34 bold True color "#f8fafc"
                add Solid("#1e5363", xsize=792, ysize=3)

                textbutton "Terima kasih. Aku akan mengulang materinya malam ini.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("review")

                textbutton "Sekarang aku tidak akan lupa arti nocturnal berkat Bima.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("joke")

                textbutton "Aku masih bingung menentukan petunjuk yang paling kuat.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("question")

                text "Balasan akan langsung muncul di percakapan grup." size 18 color "#94a3b8"
        else:
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 18

                text "MEMBACA PESAN GRUP" xalign 0.5 size 20 bold True color "#22d3ee"
                text "Pilihan balasan akan muncul setelah semua pesan selesai." xalign 0.5 text_align 0.5 xsize 700 size 30 color "#f8fafc"

    timer 3.35 action SetScreenVariable("choices_ready", True)


screen whatsapp_day_one_summary_followup(reply_choice):
    modal True
    zorder 120
    default can_dismiss = False

    add Solid("#000000c7")

    fixed at whatsapp_followup_enter:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:49" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            if reply_choice == "review":
                use whatsapp_group_text_message(
                    "Anda",
                    "Terima kasih, semuanya. Aku akan mengulang lima kata ini dan membuat contoh kalimatnya malam ini.",
                    0, 550, 125, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Bagus. Lima belas menit yang fokus lebih berguna daripada belajar lama sambil membuka banyak hal lain.",
                    135, 535, 110, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Rina",
                    "Aku juga akan mengulang sebentar malam ini. Kalau mau, nanti kita bisa membandingkan contoh kalimat.",
                    255, 525, 110, 1.85, "#d94683"
                )

            elif reply_choice == "joke":
                use whatsapp_group_text_message(
                    "Anda",
                    "Ringkasannya diterima. Setidaknya sekarang aku tidak akan lupa arti nocturnal berkat Bima.",
                    0, 550, 125, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Bima",
                    "Akhirnya pengorbanan jam tidurku diakui secara akademis!",
                    135, 500, 110, 1.05, "#ea6a16"
                )
                use whatsapp_group_text_message(
                    "Maya",
                    "Pelajari arti katanya, jangan tiru jadwal hidup contohnya.",
                    255, 500, 110, 1.85, "#7e57c2"
                )

            else:
                use whatsapp_group_text_message(
                    "Anda",
                    "Ringkasannya sudah kubaca, tapi aku masih bingung menentukan petunjuk konteks yang paling kuat. Besok boleh dibahas lagi?",
                    0, 560, 125, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Tentu. Utamakan bagian yang paling langsung menjelaskan kata target. Besok kita bahas satu contoh lagi.",
                    135, 535, 110, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Rina",
                    "Aku juga masih ragu saat petunjuknya berupa kontras. Nanti aku ikut mencatat penjelasannya.",
                    255, 525, 110, 1.85, "#d94683"
                )

            use whatsapp_group_text_message(
                "Leo",
                "Besok pukul 08.00, tempat yang sama. Materinya Structure dasar. Bawa tugas Vocabulary kalian.",
                375, 535, 105, 2.65, "#00897b"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Day One complete. Saving progress...",
                490, 430, 75, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Save selesai. Sekarang semuanya tidur.",
                575, 440, 75, 4.25, "#7e57c2"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.00 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_two_confirmation_chat():
    modal True
    zorder 120
    default can_dismiss = False

    add Solid("#000000b8")

    fixed at screen_shake:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "06:47" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Leo",
                "Pagi. Sesi Hari 2 dimulai pukul 08.00 di ruang belajar perpustakaan, meja dekat jendela. Materinya Structure dasar. Bawa tugas Vocabulary dan alat tulis.",
                0, 545, 115, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Siap. Aku berangkat sepuluh menit lagi.",
                125, 430, 80, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Siap. Bima, perhatikan waktunya baik-baik: nol-delapan-nol-nol.",
                215, 510, 90, 1.85, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Pesan diterima. Alarm, tubuh, dan jiwa sedang melakukan sinkronisasi.",
                315, 510, 95, 2.65, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Aku sudah bangun. Ini bukan pesan terjadwal.",
                420, 455, 80, 3.45, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Penjelasan tambahan itu justru membuatmu semakin mencurigakan.",
                510, 500, 90, 4.25, "#7e57c2"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pesan baru sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.20 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_two_skip_chat():
    modal True
    zorder 120
    default can_dismiss = False

    $ repeated_skip = day_1_status == "skipped"
    $ excuse_text = "Pagi, semuanya. Maaf, aku kembali tidak bisa ikut karena ada urusan keluarga mendadak. Aku tahu sudah tertinggal dua sesi. Tolong kirim materi Structure; malam ini aku mulai mengejar keduanya." if repeated_skip else "Pagi, semuanya. Maaf, hari ini aku tidak bisa ikut karena ada urusan keluarga mendadak. Kalian mulai tanpa aku, ya. Tolong kirim materi Structure; malam ini aku kerjakan latihan susulannya."
    $ leo_reply = "Baik. Tetapi ini sesi kedua yang kamu lewatkan. Hubungi aku malam ini agar kita menyusun cara mengejar Vocabulary dan Structure." if repeated_skip else "Baik. Selesaikan urusanmu lebih dulu. Setelah itu pelajari materi yang kami kirim dan kerjakan latihan susulannya."

    add Solid("#000000b8")

    fixed at whatsapp_followup_enter:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "07:03" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Anda",
                excuse_text,
                0, 550, 130, 0.25, "#128c7e", True
            )

            use whatsapp_group_text_message(
                "Rina",
                "Tidak apa-apa, [player_name]. Nanti aku foto papan dan kutandai contoh subjek serta verbanya.",
                140, 520, 90, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Aku akan mengirim ringkasan berlabel supaya tidak terlihat seperti hutan rumus.",
                240, 520, 90, 1.85, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Aku kirim hasil pindai lembar latihan. Kalau gambarnya miring, salahkan kameranya.",
                340, 520, 100, 2.65, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Semoga side quest keluarganya cepat selesai. Main quest Structure akan kami jaga!",
                450, 520, 90, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Leo",
                leo_reply,
                550, 545, 100, 4.25, "#00897b"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.20 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_three_confirmation_chat():
    modal True
    zorder 120
    default can_dismiss = False

    $ structure_item = "catatan Structure susulan" if day_2_status == "skipped" else "tugas Structure"
    $ leo_confirmation = "Sesi Reading dimulai pukul 15.30 di ruang baca lantai dua perpustakaan, meja dekat rak referensi. Bawa " + structure_item + ", alat tulis, dan satu highlighter."

    add Solid("#000000b8")

    fixed at screen_shake:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "14:12" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Leo",
                leo_confirmation,
                0, 550, 130, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Aku masih di kampus. Nanti aku langsung ke lantai dua dan menyimpan enam kursi.",
                140, 520, 90, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Gunakan tangga kiri. Lift perpustakaan sedang diperbaiki.",
                240, 500, 80, 1.85, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Kelasku selesai pukul 15.10. Aku langsung ke sana.",
                330, 475, 80, 2.65, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Quest marker: rak referensi. Reward: kemampuan menemukan main idea.",
                420, 500, 90, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Pastikan quest marker-mu tidak berbelok ke kantin.",
                520, 475, 90, 4.25, "#7e57c2"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pesan baru sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.20 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_three_skip_chat():
    modal True
    zorder 120
    default can_dismiss = False

    $ previous_skips = int(day_1_status == "skipped") + int(day_2_status == "skipped")
    $ leo_reply = "Ini sesi ketiga yang kamu lewatkan. Besok datang pukul 15.00 agar kita menyusun rencana mengejar materi." if previous_skips == 2 else ("Baik. Ini menjadi sesi kedua yang kamu lewatkan. Jangan menunda latihan susulannya setelah tugasmu selesai." if previous_skips == 1 else "Selesaikan tugasmu lebih dahulu. Malam ini pelajari ringkasan dan kerjakan latihan Reading susulan.")

    add Solid("#000000b8")

    fixed at whatsapp_followup_enter:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "14:27" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Anda",
                "Teman-teman, maaf. Aku tidak bisa ikut sesi Reading karena tenggat tugas kuliah mendadak dimajukan ke pukul 17.00. Tolong mulai tanpa aku dan kirimkan materi latihannya.",
                0, 550, 130, 0.25, "#128c7e", True
            )

            use whatsapp_group_text_message(
                "Rina",
                "Baik, [player_name]. Nanti aku foto passage dan bagian yang kami tandai.",
                140, 510, 90, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Aku akan mengirim ringkasan main idea dan supporting details.",
                240, 510, 90, 1.85, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Lembar soalnya akan kupindai. Kali ini kameraku akan kuusahakan lurus.",
                340, 520, 90, 2.65, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Selesaikan deadline side quest-mu. Party Reading akan menjaga main quest.",
                440, 510, 90, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Leo",
                leo_reply,
                540, 545, 110, 4.25, "#00897b"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.20 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_four_confirmation_chat():
    modal True
    zorder 120
    default can_dismiss = False

    $ prior_backlog = sum(int(flag) for flag in (day_1_makeup_pending, day_2_makeup_pending, day_3_makeup_pending))
    $ leo_confirmation = "Sesi Listening dimulai pukul 15.30 di Laboratorium Bahasa Gedung B lantai dua. Bawa earphone dan catatan Reading."
    if prior_backlog == 3:
        $ leo_confirmation += " [player_name], datang pukul 15.00 sesuai rencana kita."

    add Solid("#000000b8")

    fixed at screen_shake:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "14:03" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Leo",
                leo_confirmation,
                0, 550, 145, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Aku datang pukul 15.10 untuk memastikan headset laboratoriumnya berfungsi.",
                155, 510, 85, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Aku membawa earphone cadangan dan adaptor.",
                250, 460, 85, 1.85, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Jangan langsung menaikkan volume sampai maksimal.",
                345, 470, 80, 2.65, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Pemeriksaan perangkat: telinga kiri online, telinga kanan masih loading.",
                435, 510, 90, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Coba lepaskan earphone-mu dari posisi terbalik.",
                535, 470, 85, 4.25, "#7e57c2"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pesan baru sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.20 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_four_skip_chat():
    modal True
    zorder 120
    default can_dismiss = False

    $ prior_backlog = sum(int(flag) for flag in (day_1_makeup_pending, day_2_makeup_pending, day_3_makeup_pending))
    $ leo_reply = "Rencana pukul 15.00 kita tunda. Istirahatlah, lalu besok datang pukul 14.45. Empat materi tidak boleh terus menumpuk." if prior_backlog == 3 else ("Ini membuat tiga materi tertunda. Besok datang pukul 14.45 agar kita menyusun rencana sebelum sesi Structure." if prior_backlog == 2 else ("Kesehatan lebih dahulu. Setelah pulih, selesaikan dua materi tertunda itu secara berurutan." if prior_backlog == 1 else "Istirahatlah. Setelah membaik, dengarkan rekaman dan kerjakan latihan Listening susulan."))

    add Solid("#000000b8")

    fixed at whatsapp_followup_enter:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "14:18" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Anda",
                "Maaf, semuanya. Sakit kepalaku memburuk sejak siang dan aku sulit fokus pada suara. Aku tidak bisa mengikuti sesi Listening hari ini. Tolong kirim rekaman, catatan, dan latihan susulannya.",
                0, 550, 135, 0.25, "#128c7e", True
            )

            use whatsapp_group_text_message(
                "Rina",
                "Istirahat dulu, [player_name]. Aku akan mencatat bagian penting dan waktu kemunculannya.",
                145, 510, 85, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Aku kirim ringkasan tentang keyword, intent, dan informasi tersirat.",
                240, 510, 85, 1.85, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Rekaman latihan dan lembar soal akan kukirim setelah sesi.",
                335, 490, 85, 2.65, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Health bar lebih penting. Party Listening akan menjaga rekamannya.",
                430, 500, 85, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Leo",
                leo_reply,
                525, 545, 125, 4.25, "#00897b"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.20 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_two_summary_notification():
    modal True
    zorder 130

    frame at whatsapp_notification_pop:
        xalign 0.5
        ypos 54
        xsize 760
        ysize 126
        padding (20, 14)
        background Solid("#101827f2")

        hbox:
            spacing 18

            fixed:
                xsize 82
                ysize 82
                add Solid("#128c7e")
                text "WA" xalign 0.5 yalign 0.5 size 27 bold True color "#ffffff"

            vbox:
                xsize 610
                spacing 3
                text "WHATSAPP  •  SEKARANG" size 16 bold True color "#76d8c9"
                text "Seven Days to TOEFL" size 25 bold True color "#ffffff"
                text "Leo: Ringkasan Structure Hari 2 sudah kukirim." xsize 590 size 19 color "#d9e4e8"

    timer 1.60 action Return(True)


screen whatsapp_day_two_summary_chat():
    modal True
    zorder 120
    default choices_ready = False

    $ structure_summary = "STRUCTURE HARI 2\n1. Cari subject dan finite verb.\n2. Sisihkan modifier saat mencari inti.\n3. Cocokkan singular/plural dengan verb.\n4. Hubungkan dependent dan main clause.\n5. Periksa bagian yang hilang atau berlebih.\nPola: CLAUSE → SUBJECT → VERB → AGREEMENT\nTugas: tandai S dan V dalam lima kalimat."
    $ review_choice_text = "Terima kasih. Aku akan mempelajari ringkasan dan mengerjakan latihan susulannya." if day_2_status == "skipped" else "Terima kasih. Aku akan menandai subject dan verb lagi malam ini."

    add Solid("#000000c7")

    fixed at screen_shake:
        xpos 100
        ypos 40
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:38" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Leo",
                structure_summary,
                0, 560, 270, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Subject kutandai biru, sedangkan verb kutandai merah.",
                280, 500, 85, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Catatannya sudah kurapikan agar mudah dibaca.",
                375, 520, 85, 1.75, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Aku memahami Structure hari ini. Semoga.",
                470, 455, 75, 2.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Kalimat pertama benar. Kepastiannya belum teruji.",
                555, 455, 90, 3.15, "#2563eb"
            )

        if choices_ready:
            text "Pilih balasan di sebelah kanan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pesan baru sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    frame:
        xpos 900
        ypos 140
        xsize 880
        ysize 800
        padding (44, 44)
        background Solid("#0b1f2ef2")

        if choices_ready:
            vbox at whatsapp_message_fade(0.0):
                xfill True
                spacing 16

                text "PILIH BALASAN" size 20 bold True color "#22d3ee"
                text "Apa yang akan dikirim [player_name] ke grup?" xsize 792 size 34 bold True color "#f8fafc"
                add Solid("#1e5363", xsize=792, ysize=3)

                textbutton review_choice_text:
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("review")

                textbutton "Kalimat pertama Bima benar, tetapi kepastiannya masih membutuhkan bukti.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("joke")

                textbutton "Aku masih bingung membedakan verb main clause dan relative clause.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("question")

                text "Balasan akan langsung muncul di percakapan grup." size 18 color "#94a3b8"
        else:
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 18

                text "MEMBACA PESAN GRUP" xalign 0.5 size 20 bold True color "#22d3ee"
                text "Pilihan balasan akan muncul setelah semua pesan selesai." xalign 0.5 text_align 0.5 xsize 700 size 30 color "#f8fafc"

    timer 3.55 action SetScreenVariable("choices_ready", True)


screen whatsapp_day_two_summary_followup(reply_choice):
    modal True
    zorder 120
    default can_dismiss = False

    $ review_reply = "Terima kasih. Aku akan mempelajari ringkasan ini dan mengerjakan latihan susulannya." if day_2_status == "skipped" else "Terima kasih. Aku akan menandai subject dan verb lagi malam ini."

    add Solid("#000000c7")

    fixed at whatsapp_followup_enter:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:40" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            if reply_choice == "review":
                use whatsapp_group_text_message(
                    "Anda",
                    review_reply,
                    0, 550, 120, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Bagus. Cari inti subject dan verb sebelum memeriksa bagian lain.",
                    130, 520, 105, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Rina",
                    "Kalau mau, kirim satu jawabanmu nanti supaya bisa kita bandingkan.",
                    245, 520, 105, 1.85, "#d94683"
                )

            elif reply_choice == "joke":
                use whatsapp_group_text_message(
                    "Anda",
                    "Kalimat pertama Bima benar, tetapi kepastiannya masih membutuhkan bukti.",
                    0, 550, 120, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Bima",
                    "Setidaknya secara grammar aku sudah lulus!",
                    130, 475, 105, 1.05, "#ea6a16"
                )
                use whatsapp_group_text_message(
                    "Maya",
                    "Sayangnya kita sedang menilai pemahaman, bukan keberanian.",
                    245, 500, 105, 1.85, "#7e57c2"
                )

            else:
                use whatsapp_group_text_message(
                    "Anda",
                    "Aku masih bingung membedakan verb main clause dan relative clause.",
                    0, 550, 125, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Tandai batas clause lebih dahulu. Setiap finite clause memiliki pasangan subject dan verb sendiri.",
                    135, 545, 110, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Reza",
                    "Aku memakai garis miring antarklausa. Main verb jadi lebih mudah terlihat.",
                    255, 520, 105, 1.85, "#2563eb"
                )

            use whatsapp_group_text_message(
                "Leo",
                "Besok, Senin pukul 15.30 di perpustakaan. Materinya Reading: main idea dan supporting details.",
                375, 545, 105, 2.65, "#00897b"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Day Two complete. Subject: kita. Verb: survived.",
                490, 460, 75, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Untuk sekali ini, analisismu benar.",
                575, 435, 75, 4.25, "#7e57c2"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.00 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_three_summary_notification():
    modal True
    zorder 130

    frame at whatsapp_notification_pop:
        xalign 0.5
        ypos 54
        xsize 760
        ysize 126
        padding (20, 14)
        background Solid("#101827f2")

        hbox:
            spacing 18

            fixed:
                xsize 82
                ysize 82
                add Solid("#128c7e")
                text "WA" xalign 0.5 yalign 0.5 size 27 bold True color "#ffffff"

            vbox:
                xsize 610
                spacing 3
                text "WHATSAPP  •  SEKARANG" size 16 bold True color "#76d8c9"
                text "Seven Days to TOEFL" size 25 bold True color "#ffffff"
                text "Leo: Ringkasan Reading Hari 3 sudah kukirim." xsize 590 size 19 color "#d9e4e8"

    timer 1.60 action Return(True)


screen whatsapp_day_three_summary_chat():
    modal True
    zorder 120
    default choices_ready = False

    $ reading_summary = "READING HARI 3\n1. Kenali jenis pertanyaannya.\n2. Main idea harus mencakup seluruh passage.\n3. Detail harus cocok dengan bukti atau parafrasanya.\n4. Uji reference dan vocabulary di dalam konteks.\n5. Inference tidak boleh memakai asumsi tanpa dukungan teks.\nPola: QUESTION → EVIDENCE → ANSWER\nTugas: tentukan main idea dan dua supporting details."
    $ review_choice_text = "Terima kasih. Aku akan mempelajari ringkasan dan mengerjakan latihan Reading susulannya." if day_3_status == "skipped" else "Ringkasannya jelas. Aku akan menandai main idea dan detailnya malam ini."

    add Solid("#000000c7")

    fixed at screen_shake:
        xpos 100
        ypos 40
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:26" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Leo",
                reading_summary,
                0, 560, 300, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Main idea kutandai biru dan supporting details kuning.",
                310, 500, 85, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Aku menerapkan highlighter dengan strategi cakupan maksimal.",
                405, 500, 90, 1.85, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Kamu menandai hampir seluruh paragraf. Itu bukan strategi.",
                505, 500, 90, 2.65, "#7e57c2"
            )

        if choices_ready:
            text "Pilih balasan di sebelah kanan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pesan baru sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    frame:
        xpos 900
        ypos 140
        xsize 880
        ysize 800
        padding (44, 44)
        background Solid("#0b1f2ef2")

        if choices_ready:
            vbox at whatsapp_message_fade(0.0):
                xfill True
                spacing 16

                text "PILIH BALASAN" size 20 bold True color "#22d3ee"
                text "Apa yang akan dikirim [player_name] ke grup?" xsize 792 size 34 bold True color "#f8fafc"
                add Solid("#1e5363", xsize=792, ysize=3)

                textbutton review_choice_text:
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("review")

                textbutton "Main idea obrolan ini: Bima belum memahami fungsi highlighter.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("joke")

                textbutton "Aku masih bingung membedakan main idea yang terlalu luas dan terlalu sempit.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("question")

                text "Balasan akan langsung muncul di percakapan grup." size 18 color "#94a3b8"
        else:
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 18

                text "MEMBACA PESAN GRUP" xalign 0.5 size 20 bold True color "#22d3ee"
                text "Pilihan balasan akan muncul setelah semua pesan selesai." xalign 0.5 text_align 0.5 xsize 700 size 30 color "#f8fafc"

    timer 3.05 action SetScreenVariable("choices_ready", True)


screen whatsapp_day_three_summary_followup(reply_choice):
    modal True
    zorder 120
    default can_dismiss = False

    $ review_reply = "Terima kasih. Aku akan mempelajari ringkasan ini dan mengerjakan latihan Reading susulannya." if day_3_status == "skipped" else "Ringkasannya jelas. Aku akan menandai main idea dan supporting details malam ini."

    add Solid("#000000c7")

    fixed at whatsapp_followup_enter:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:28" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            if reply_choice == "review":
                use whatsapp_group_text_message(
                    "Anda",
                    review_reply,
                    0, 550, 120, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Bagus. Pastikan setiap detail yang kamu pilih benar-benar mendukung main idea.",
                    130, 530, 105, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Rina",
                    "Kalau perlu, besok kita bandingkan hasil penandaan.",
                    245, 480, 105, 1.85, "#d94683"
                )

            elif reply_choice == "joke":
                use whatsapp_group_text_message(
                    "Anda",
                    "Main idea obrolan malam ini: Bima masih belum memahami fungsi highlighter.",
                    0, 550, 120, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Bima",
                    "Semua bagian penting kalau kita membacanya dengan hati.",
                    130, 490, 105, 1.05, "#ea6a16"
                )
                use whatsapp_group_text_message(
                    "Maya",
                    "Highlighter-mu tidak bekerja berdasarkan hati.",
                    245, 475, 105, 1.85, "#7e57c2"
                )

            else:
                use whatsapp_group_text_message(
                    "Anda",
                    "Aku masih bingung membedakan main idea yang terlalu luas dan terlalu sempit.",
                    0, 550, 125, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Jawaban terlalu luas membahas hal di luar passage. Jawaban terlalu sempit hanya mewakili satu detail.",
                    135, 545, 110, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Reza",
                    "Aku menguji apakah pilihan itu masih cocok untuk semua bagian passage.",
                    255, 520, 105, 1.85, "#2563eb"
                )

            use whatsapp_group_text_message(
                "Leo",
                "Besok, Selasa pukul 15.30 di Laboratorium Bahasa Gedung B lantai dua. Materinya Listening. Bawa earphone.",
                375, 545, 110, 2.65, "#00897b"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Day Three complete. Telinga: semoga online.",
                495, 475, 75, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Isi daya otakmu juga.",
                580, 420, 70, 4.25, "#7e57c2"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.00 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_four_summary_notification():
    modal True
    zorder 130

    frame at whatsapp_notification_pop:
        xalign 0.5
        ypos 54
        xsize 760
        ysize 126
        padding (20, 14)
        background Solid("#101827f2")

        hbox:
            spacing 18

            fixed:
                xsize 82
                ysize 82
                add Solid("#128c7e")
                text "WA" xalign 0.5 yalign 0.5 size 27 bold True color "#ffffff"

            vbox:
                xsize 610
                spacing 3
                text "WHATSAPP  •  SEKARANG" size 16 bold True color "#76d8c9"
                text "Seven Days to TOEFL" size 25 bold True color "#ffffff"
                text "Leo: Ringkasan Listening Hari 4 sudah kukirim." xsize 590 size 19 color "#d9e4e8"

    timer 1.60 action Return(True)


screen whatsapp_day_four_summary_chat():
    modal True
    zorder 120
    default choices_ready = False

    $ listening_summary = "LISTENING HARI 4\n1. Preview pertanyaan dan pilihan.\n2. Tangkap keyword, intent, dan informasi penting.\n3. Perhatikan negative, contrast, dan suggestion.\n4. Jawaban biasanya berupa parafrasa.\n5. Jika kehilangan satu kata, lanjutkan mendengarkan.\nPola: LISTEN → KEYWORDS → INTENT → ANSWER\nTugas: tiga dialog; catat keyword, intent, dan next action."
    $ review_choice_text = "Terima kasih. Aku akan mendengarkan rekaman dan mengerjakan latihan Listening susulannya." if day_4_status == "skipped" else "Ringkasannya jelas. Aku akan berlatih mencatat keyword tanpa menulis seluruh kalimat."

    add Solid("#000000c7")

    fixed at screen_shake:
        xpos 100
        ypos 40
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:18" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Leo",
                listening_summary,
                0, 560, 300, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Aku menambahkan waktu untuk informasi penting.",
                310, 460, 70, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Catatan singkat mencegah audio berikutnya terlewat.",
                390, 475, 70, 1.75, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Otakku buffering pada dialog kedua.",
                470, 430, 70, 2.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Laboratorium tidak menyediakan tombol refresh.",
                550, 455, 70, 3.15, "#7e57c2"
            )

        if choices_ready:
            text "Pilih balasan di sebelah kanan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pesan baru sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    frame:
        xpos 900
        ypos 140
        xsize 880
        ysize 800
        padding (44, 44)
        background Solid("#0b1f2ef2")

        if choices_ready:
            vbox at whatsapp_message_fade(0.0):
                xfill True
                spacing 16

                text "PILIH BALASAN" size 20 bold True color "#22d3ee"
                text "Apa yang akan dikirim [player_name] ke grup?" xsize 792 size 34 bold True color "#f8fafc"
                add Solid("#1e5363", xsize=792, ysize=3)

                textbutton review_choice_text:
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("review")

                textbutton "Masalah utama sesi tadi bukan audionya, tetapi otak Bima yang buffering.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("joke")

                textbutton "Aku masih sulit membedakan informasi langsung dan maksud yang hanya tersirat.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("question")

                text "Balasan akan langsung muncul di percakapan grup." size 18 color "#94a3b8"
        else:
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 18

                text "MEMBACA PESAN GRUP" xalign 0.5 size 20 bold True color "#22d3ee"
                text "Pilihan balasan akan muncul setelah semua pesan selesai." xalign 0.5 text_align 0.5 xsize 700 size 30 color "#f8fafc"

    timer 3.55 action SetScreenVariable("choices_ready", True)


screen whatsapp_day_four_summary_followup(reply_choice):
    modal True
    zorder 120
    default can_dismiss = False

    $ total_backlog = sum(int(flag) for flag in (day_1_makeup_pending, day_2_makeup_pending, day_3_makeup_pending, day_4_makeup_pending))
    $ review_reply = "Terima kasih. Aku akan mendengarkan rekaman ini dan mengerjakan latihan Listening susulannya." if day_4_status == "skipped" else "Ringkasannya jelas. Aku akan berlatih mencatat keyword tanpa menulis seluruh kalimat."
    $ day_five_schedule = "Besok, Rabu pukul 15.30 di perpustakaan: Structure lanjutan—parallel structure dan reduced clauses. Bawa catatan."
    if total_backlog >= 3:
        $ day_five_schedule += " [player_name], datang pukul 14.45."

    add Solid("#000000c7")

    fixed at whatsapp_followup_enter:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:20" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            if reply_choice == "review":
                use whatsapp_group_text_message(
                    "Anda",
                    review_reply,
                    0, 550, 120, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Bagus. Catatan terlalu panjang justru membuatmu kehilangan audio berikutnya.",
                    130, 530, 105, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Rina",
                    "Aku memakai singkatan untuk place, time, dan action.",
                    245, 480, 105, 1.85, "#d94683"
                )

            elif reply_choice == "joke":
                use whatsapp_group_text_message(
                    "Anda",
                    "Masalah utama sesi tadi bukan audionya, tetapi otak Bima yang buffering.",
                    0, 550, 120, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Bima",
                    "Buffering adalah bagian dari proses pembelajaran.",
                    130, 490, 105, 1.05, "#ea6a16"
                )
                use whatsapp_group_text_message(
                    "Maya",
                    "Prosesmu terlalu sering berhenti di sembilan puluh sembilan persen.",
                    245, 510, 105, 1.85, "#7e57c2"
                )

            else:
                use whatsapp_group_text_message(
                    "Anda",
                    "Aku masih sulit membedakan informasi langsung dan maksud yang hanya tersirat.",
                    0, 550, 125, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Informasi langsung dinyatakan jelas. Intent terlihat dari respons, tone, atau tindakan yang disarankan.",
                    135, 545, 110, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Reza",
                    "Aku menghapus pilihan yang bertentangan dengan respons pembicara kedua.",
                    255, 520, 105, 1.85, "#2563eb"
                )

            use whatsapp_group_text_message(
                "Leo",
                day_five_schedule,
                375, 545, 120, 2.65, "#00897b"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Day Four complete. Audio tersimpan.",
                505, 430, 65, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Semoga memorinya tidak corrupt.",
                580, 420, 70, 4.25, "#7e57c2"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.00 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_five_confirmation_chat(prior_backlog=0):
    modal True
    zorder 120
    default can_dismiss = False

    $ leo_confirmation = "Rabu pukul 15.30 kita bertemu di perpustakaan lantai dua, meja dekat jendela. Materinya Structure Lanjutan: parallel structure dan reduced clauses. Bawa catatan Structure dasar."
    if prior_backlog >= 3:
        $ leo_confirmation += " [player_name], datang pukul 14.45 untuk membahas latihan susulan lebih dulu."

    add Solid("#000000b8")

    fixed at screen_shake:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "14:06" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Leo",
                leo_confirmation,
                0, 555, 165, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Aku membawa ringkasan pola dasar supaya kita bisa membandingkannya.",
                175, 505, 85, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Aku sudah menyiapkan lima kalimat untuk diuji bentuk paralelnya.",
                270, 505, 85, 1.85, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Jangan menghapus relative clause sebelum memastikan voice-nya.",
                365, 505, 85, 2.65, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Reduced clause berarti ukuran kalimat dikompres tanpa menurunkan kualitas?",
                460, 520, 95, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Kurang lebih, asalkan kamu tidak menghapus subject secara acak.",
                565, 490, 85, 4.25, "#7e57c2"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pesan baru sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.20 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_five_skip_chat(prior_backlog=0, current_backlog=0):
    modal True
    zorder 120
    default can_dismiss = False

    $ backlog_after_skip = current_backlog if current_backlog > 0 else prior_backlog + 1
    if prior_backlog >= 3:
        $ leo_reply = "Pertemuan pukul 14.45 hari ini juga ikut batal. Keselamatan lebih penting. Sekarang ada {} materi tertunda; besok datang pukul 14.45 sebelum Review Terpadu.".format(backlog_after_skip)
    elif backlog_after_skip >= 3:
        $ leo_reply = "Keselamatan lebih penting. Sekarang ada {} materi tertunda; besok datang pukul 14.45 sebelum Review Terpadu agar kita mengaturnya.".format(backlog_after_skip)
    elif backlog_after_skip == 2:
        $ leo_reply = "Jangan menerobos genangan. Setelah aman, kerjakan dua materi tertunda itu secara berurutan."
    else:
        $ leo_reply = "Tetap di rumah dan pantau kondisi jalan. Catatan serta latihan Structure Lanjutan akan kukirim."

    add Solid("#000000b8")

    fixed at whatsapp_followup_enter:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "14:19" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Anda",
                "Maaf, aku tidak bisa datang. Jalan di kompleks rumahku tergenang dan belum aman untuk dilewati. Aku akan tetap di rumah sampai airnya surut.",
                0, 555, 135, 0.25, "#128c7e", True
            )

            use whatsapp_group_text_message(
                "Rina",
                "Jangan memaksakan diri. Aku akan memotret papan dan mengirim catatannya.",
                145, 505, 80, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Arus di jalan yang tergenang sulit diprediksi. Tunggu sampai benar-benar aman.",
                235, 510, 80, 1.85, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Aku akan menandai contoh active dan passive reduction untukmu.",
                325, 495, 80, 2.65, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Jangan mencoba membuka jalur rahasia dengan perahu karet.",
                415, 475, 75, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Leo",
                leo_reply,
                500, 550, 145, 4.25, "#00897b"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.20 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_five_summary_notification():
    modal True
    zorder 130

    frame at whatsapp_notification_pop:
        xalign 0.5
        ypos 54
        xsize 760
        ysize 126
        padding (20, 14)
        background Solid("#101827f2")

        hbox:
            spacing 18

            fixed:
                xsize 82
                ysize 82
                add Solid("#128c7e")
                text "WA" xalign 0.5 yalign 0.5 size 27 bold True color "#ffffff"

            vbox:
                xsize 610
                spacing 3
                text "WHATSAPP  •  SEKARANG" size 16 bold True color "#76d8c9"
                text "Seven Days to TOEFL" size 25 bold True color "#ffffff"
                text "Leo: Ringkasan Structure Lanjutan Hari 5 sudah kukirim." xsize 590 size 19 color "#d9e4e8"

    timer 1.60 action Return(True)


screen whatsapp_day_five_summary_chat():
    modal True
    zorder 120
    default choices_ready = False

    $ structure_advanced_summary = "STRUCTURE LANJUTAN HARI 5\n1. Parallel: same form dan same function.\n2. Paired conjunctions: bentuk di kedua sisi harus setara.\n3. Active reduced clause memakai V-ing.\n4. Passive reduced clause memakai V3.\n5. Adverb clause dapat direduksi jika subject-nya sama.\nPola: FORM → FUNCTION → VOICE → CHECK\nTugas: perbaiki lima kalimat."
    $ review_choice_text = "Terima kasih. Aku akan mempelajari catatan dan mengerjakan Structure Lanjutan susulan." if day_5_status == "skipped" else "Ringkasannya jelas. Aku akan memeriksa form, function, dan voice secara berurutan."

    add Solid("#000000c7")

    fixed at screen_shake:
        xpos 100
        ypos 40
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:24" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            use whatsapp_group_text_message(
                "Leo",
                structure_advanced_summary,
                0, 560, 305, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Aku menambahkan warna berbeda untuk active V-ing dan passive V3.",
                315, 500, 75, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Subject check mencegah adverb clause direduksi secara keliru.",
                400, 500, 75, 1.75, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Hari ini kalimat panjang masuk mesin kompresi.",
                485, 455, 70, 2.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Dan mesin itu tetap membutuhkan pemeriksaan voice.",
                565, 455, 70, 3.15, "#7e57c2"
            )

        if choices_ready:
            text "Pilih balasan di sebelah kanan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pesan baru sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    frame:
        xpos 900
        ypos 140
        xsize 880
        ysize 800
        padding (44, 44)
        background Solid("#0b1f2ef2")

        if choices_ready:
            vbox at whatsapp_message_fade(0.0):
                xfill True
                spacing 16

                text "PILIH BALASAN" size 20 bold True color "#22d3ee"
                text "Apa yang akan dikirim [player_name] ke grup?" xsize 792 size 34 bold True color "#f8fafc"
                add Solid("#1e5363", xsize=792, ysize=3)

                textbutton review_choice_text:
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("review")

                textbutton "Berarti Bima hari ini resmi menjadi teknisi kompresi klausa.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("joke")

                textbutton "Aku masih sering tertukar menentukan active V-ing dan passive V3.":
                    xfill True
                    ysize 150
                    padding (28, 22)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    text_color "#ecfeff"
                    text_size 24
                    action Return("question")

                text "Balasan akan langsung muncul di percakapan grup." size 18 color "#94a3b8"
        else:
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 18

                text "MEMBACA PESAN GRUP" xalign 0.5 size 20 bold True color "#22d3ee"
                text "Pilihan balasan akan muncul setelah semua pesan selesai." xalign 0.5 text_align 0.5 xsize 700 size 30 color "#f8fafc"

    timer 3.55 action SetScreenVariable("choices_ready", True)


screen whatsapp_day_five_summary_followup(reply_choice, current_backlog=0):
    modal True
    zorder 120
    default can_dismiss = False

    $ review_reply = "Terima kasih. Aku akan mempelajari catatan dan mengerjakan Structure Lanjutan susulan." if day_5_status == "skipped" else "Ringkasannya jelas. Aku akan memeriksa form, function, dan voice secara berurutan."
    $ day_six_schedule = "Besok, Kamis pukul 15.30 di perpustakaan: Review Terpadu Vocabulary, Structure, Reading, dan Listening. Bawa seluruh catatan."
    if current_backlog >= 3:
        $ day_six_schedule += " [player_name], datang pukul 14.45 untuk latihan susulan."

    add Solid("#000000c7")

    fixed at whatsapp_followup_enter:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "21:26" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 650

            if reply_choice == "review":
                use whatsapp_group_text_message(
                    "Anda",
                    review_reply,
                    0, 550, 120, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Bagus. Periksa fungsi setiap unsur sebelum membandingkan bentuknya.",
                    130, 520, 105, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Rina",
                    "Aku akan mengirim versi catatan dengan penanda warnanya.",
                    245, 490, 105, 1.85, "#d94683"
                )

            elif reply_choice == "joke":
                use whatsapp_group_text_message(
                    "Anda",
                    "Berarti Bima hari ini resmi menjadi teknisi kompresi klausa.",
                    0, 550, 120, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Bima",
                    "Aku menerima gelar itu selama tidak ada ujian praktik mesin.",
                    130, 505, 105, 1.05, "#ea6a16"
                )
                use whatsapp_group_text_message(
                    "Maya",
                    "Lisensimu ditahan sampai kamu bisa membedakan active dan passive.",
                    245, 520, 105, 1.85, "#7e57c2"
                )

            else:
                use whatsapp_group_text_message(
                    "Anda",
                    "Aku masih sering tertukar menentukan active V-ing dan passive V3.",
                    0, 550, 125, 0.25, "#128c7e", True
                )
                use whatsapp_group_text_message(
                    "Leo",
                    "Tanyakan: noun itu melakukan tindakan atau menerima tindakan? Melakukan berarti V-ing; menerima berarti V3.",
                    135, 550, 115, 1.05, "#00897b"
                )
                use whatsapp_group_text_message(
                    "Reza",
                    "Aku juga memeriksa apakah bentuk panjangnya memakai active atau passive voice.",
                    260, 520, 105, 1.85, "#2563eb"
                )

            use whatsapp_group_text_message(
                "Leo",
                day_six_schedule,
                380, 550, 125, 2.65, "#00897b"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Besok semua materi masuk satu party.",
                515, 480, 65, 3.45, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Semoga party itu membaca catatan.",
                585, 455, 65, 4.25, "#7e57c2"
            )

        if can_dismiss:
            text "Ketuk layar untuk melanjutkan" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Menunggu balasan..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.00 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen whatsapp_day_six_location_update(backlog_count=0):
    modal True
    zorder 120
    default can_dismiss = False

    $ leo_final = "Bawa seluruh catatan dan earphone. Sesi utama tetap pukul 15.30."
    if backlog_count >= 3:
        $ leo_final += " [player_name], check-in pukul 14.45 juga dipindahkan ke kafe."

    add Solid("#000000c7")

    fixed at screen_shake:
        xalign 0.5
        yalign 0.5
        xsize 690
        ysize 1000

        add "gui/whatsapp_phone.svg"

        text "13:52" xpos 57 ypos 31 size 16 bold True color "#ffffff"
        text "Seven Days to TOEFL" xpos 158 ypos 82 size 23 bold True color "#ffffff"
        text "6 anggota • grup belajar" xpos 158 ypos 119 size 15 color "#d7f2ec"
        text "HARI INI" xpos 316 ypos 188 size 15 bold True color "#55706a"

        fixed:
            xpos 40
            ypos 215
            xsize 610
            ysize 670

            use whatsapp_group_text_message(
                "Leo",
                "Perubahan lokasi. Ruang diskusi perpustakaan ditutup sementara untuk pemeriksaan listrik. Review dipindahkan ke Kafe Ruang Sela, seberang gerbang timur kampus.",
                0, 565, 145, 0.25, "#00897b"
            )

            use whatsapp_group_text_message(
                "Rina",
                "Aku sudah memesan meja panjang. Tempatnya tenang, ada stopkontak, dan yang terpenting: ada dessert.",
                155, 535, 105, 1.05, "#d94683"
            )

            use whatsapp_group_text_message(
                "Reza",
                "Pin lokasi terkirim. Dari gerbang timur sekitar tujuh menit berjalan kaki.",
                270, 510, 90, 1.85, "#2563eb"
            )

            use whatsapp_group_text_message(
                "Bima",
                "Review di kafe? Akhirnya ada healing area sebelum final boss.",
                370, 520, 82, 2.65, "#ea6a16"
            )

            use whatsapp_group_text_message(
                "Maya",
                "Healing, bukan kesempatan memesan gula dengan sedikit kopi.",
                462, 515, 82, 3.45, "#7e57c2"
            )

            use whatsapp_group_text_message(
                "Leo",
                leo_final,
                554, 565, 108, 4.25, "#00897b"
            )

        if can_dismiss:
            text "Ketuk layar untuk membuka rute" xpos 121 ypos 895 size 20 bold True color "#128c7e" at whatsapp_message_fade(0.0)
        else:
            text "Pembaruan lokasi sedang masuk..." xpos 121 ypos 895 size 20 color "#82938e"

    timer 5.10 action SetScreenVariable("can_dismiss", True)
    key "dismiss" action If(can_dismiss, Return(True), NullAction())


screen day_six_travel_choice(backlog_count=0):
    modal True
    zorder 110

    add Solid("#140f0bc7")

    frame at day_six_panel_enter:
        xalign 0.5
        yalign 0.5
        xsize 1320
        padding (54, 46)
        background Solid("#241a14f2")

        vbox:
            spacing 30

            vbox:
                xalign 0.5
                spacing 7
                text "HARI 6  •  PERJALANAN KE KAFE" xalign 0.5 size 19 bold True color "#fbbf24"
                text "Pilih rute perjalanan" xalign 0.5 size 42 bold True color "#fff7ed"
                if backlog_count >= 3:
                    text "Kamu berangkat lebih awal untuk check-in pukul 14.45." xalign 0.5 size 21 color "#fed7aa"
                else:
                    text "Kedua rute tiba sebelum Review dimulai pukul 15.30." xalign 0.5 size 21 color "#d6c7ba"

            hbox:
                xalign 0.5
                spacing 36

                button at day_six_card_enter(0.08):
                    xsize 570
                    ysize 280
                    padding (34, 30)
                    background Solid("#173f35ee")
                    hover_background Solid("#166534")
                    action Return("park")

                    vbox:
                        spacing 14
                        text "RUTE 01  •  SANTAI" size 20 bold True color "#86efac"
                        text "LEWAT TAMAN" size 36 bold True color "#f0fdf4"
                        add Solid("#4ade80") xsize 110 ysize 4
                        text "Jalan lebih tenang di bawah pepohonan." xsize 480 size 23 color "#dcfce7"
                        text "Temui Rina dan Maya di persimpangan." size 18 color "#86efac"

                button at day_six_card_enter(0.16):
                    xsize 570
                    ysize 280
                    padding (34, 30)
                    background Solid("#153147ee")
                    hover_background Solid("#075985")
                    action Return("main_road")

                    vbox:
                        spacing 14
                        text "RUTE 02  •  LANGSUNG" size 20 bold True color "#7dd3fc"
                        text "JALAN UTAMA" size 36 bold True color "#f0f9ff"
                        add Solid("#38bdf8") xsize 110 ysize 4
                        text "Rute tercepat melewati gerbang timur." xsize 480 size 23 color "#e0f2fe"
                        text "Susul Reza dan Bima yang membawa peta." size 18 color "#7dd3fc"


screen day_six_cafe_drink_choice():
    modal True
    zorder 110

    add Solid("#140f0bc7")

    frame at day_six_panel_enter:
        xalign 0.5
        yalign 0.5
        xsize 1460
        padding (48, 42)
        background Solid("#2b1d14f2")

        vbox:
            spacing 28

            vbox:
                xalign 0.5
                spacing 7
                text "KAFE RUANG SELA" xalign 0.5 size 19 bold True color "#fbbf24"
                text "Pilih minuman healing-mu" xalign 0.5 size 40 bold True color "#fff7ed"
                text "Rina sudah memesannya; pilihanmu memengaruhi obrolan, bukan skor akademik." xalign 0.5 size 20 color "#d6c7ba"

            hbox:
                xalign 0.5
                spacing 24

                button at day_six_card_enter(0.06):
                    xsize 420
                    ysize 300
                    padding (30, 28)
                    background Solid("#60401fee")
                    hover_background Solid("#92400e")
                    action Return("tea")

                    vbox:
                        xalign 0.5
                        spacing 14
                        text "♨" at day_six_cup_float xalign 0.5 size 58 color "#fde68a"
                        text "TEH LEMON HANGAT" xalign 0.5 text_align 0.5 size 29 bold True color "#fffbeb"
                        text "Tenang +1" xalign 0.5 size 20 color "#fde68a"
                        text "Hangat, ringan, dan tidak mengajak jantung sprint." xalign 0.5 text_align 0.5 xsize 350 size 19 color "#fef3c7"

                button at day_six_card_enter(0.14):
                    xsize 420
                    ysize 300
                    padding (30, 28)
                    background Solid("#4b2b24ee")
                    hover_background Solid("#7c2d12")
                    action Return("chocolate")

                    vbox:
                        xalign 0.5
                        spacing 14
                        text "●" at day_six_cup_float xalign 0.5 size 58 color "#fdba74"
                        text "COKELAT PANAS" xalign 0.5 text_align 0.5 size 29 bold True color "#fff7ed"
                        text "Semangat +1" xalign 0.5 size 20 color "#fdba74"
                        text "Manis secukupnya untuk menghadapi lima tantangan." xalign 0.5 text_align 0.5 xsize 350 size 19 color "#ffedd5"

                button at day_six_card_enter(0.22):
                    xsize 420
                    ysize 300
                    padding (30, 28)
                    background Solid("#243b3bee")
                    hover_background Solid("#115e59")
                    action Return("coffee")

                    vbox:
                        xalign 0.5
                        spacing 14
                        text "◆" at day_six_cup_float xalign 0.5 size 58 color "#99f6e4"
                        text "ES KOPI SUSU" xalign 0.5 text_align 0.5 size 29 bold True color "#f0fdfa"
                        text "Fokus +1" xalign 0.5 size 20 color "#99f6e4"
                        text "Patch sederhana untuk RAM yang mulai penuh." xalign 0.5 text_align 0.5 xsize 350 size 19 color "#ccfbf1"


screen day_six_cafe_challenge(question_number, challenge_title, skill_label, prompt, option_a, option_b, option_c, hint_text=None, boss=False):
    modal True
    zorder 110
    default hint_visible = False

    $ accent = {"VOCABULARY": "#34d399", "STRUCTURE": "#22d3ee", "MIXED": "#fbbf24"}.get(skill_label, "#fbbf24")
    $ accumulated_score = day_1_vocab_score + day_2_structure_score + day_3_reading_score + day_4_listening_score + day_5_structure_score + extra_practice_score
    $ hint_level = study_hint_level(accumulated_score)

    add Solid("#120d09de")

    frame at day_six_panel_enter:
        xalign 0.5
        yalign 0.5
        xsize 1280
        ysize 900
        padding (48, 38)
        background Solid("#261b15f7")

        vbox:
            spacing 18

            fixed:
                xsize 1184
                ysize 34
                text "REVIEW RUN  •  CHALLENGE [question_number]/5" size 20 bold True color accent
                text "SKOR [day_6_review_score]/50  •  BENAR BERUNTUN: [day_6_review_streak]" xalign 1.0 size 20 bold True color "#fde68a"

            fixed:
                xsize 1184
                ysize 10
                add Solid("#4b3a31") xsize 1184 ysize 10
                add Solid(accent) xsize int(1184 * question_number / 5.0) ysize 10

            hbox:
                xfill True
                text challenge_title size 37 bold True color "#fff7ed" substitute False
                if boss:
                    text "FINAL COMBO" xalign 1.0 size 19 bold True color "#fbbf24"
                else:
                    text skill_label xalign 1.0 size 19 bold True color accent substitute False

            text prompt:
                xsize 1184
                size 31
                bold True
                color "#f8fafc"
                line_spacing 5
                substitute False

            if day == 7 and hint_text and hint_level > 0:
                textbutton ("SEMBUNYIKAN PETUNJUK" if hint_visible else "BUKA PETUNJUK"):
                    xalign 1.0
                    xsize 290
                    ysize 52
                    background Solid("#4a3527")
                    hover_background Solid("#6b4b35")
                    text_color "#fed7aa"
                    text_size 18
                    action SetScreenVariable("hint_visible", not hint_visible)

                if hint_visible:
                    frame:
                        xfill True
                        padding (22, 14)
                        background Solid("#3b2a20")
                        text hint_text xsize 1140 size 21 color "#fed7aa" substitute False
            elif day == 7 and hint_text:
                text "HINT TERKUNCI • Akumulasi skor sebelumnya belum mencapai 30 poin." xalign 1.0 size 16 color "#cbd5e1"

            add Solid("#5b4538") xsize 1184 ysize 2

            button at day_six_card_enter(0.05):
                xfill True
                ysize 92
                padding (24, 16)
                background Solid("#3b2b24")
                hover_background Solid("#7c4a2d")
                action Return("a")
                text ("A.  " + option_a) xsize 1125 yalign 0.5 size 24 color "#fff7ed" substitute False

            button at day_six_card_enter(0.10):
                xfill True
                ysize 92
                padding (24, 16)
                background Solid("#3b2b24")
                hover_background Solid("#7c4a2d")
                action Return("b")
                text ("B.  " + option_b) xsize 1125 yalign 0.5 size 24 color "#fff7ed" substitute False

            button at day_six_card_enter(0.15):
                xfill True
                ysize 92
                padding (24, 16)
                background Solid("#3b2b24")
                hover_background Solid("#7c4a2d")
                action Return("c")
                text ("C.  " + option_c) xsize 1125 yalign 0.5 size 24 color "#fff7ed" substitute False


screen day_six_reading_challenge(question_number, passage_title, passage, prompt, option_a, option_b, option_c, hint_text=None):
    modal True
    zorder 110
    default hint_visible = False
    $ accumulated_score = day_1_vocab_score + day_2_structure_score + day_3_reading_score + day_4_listening_score + day_5_structure_score + extra_practice_score
    $ hint_level = study_hint_level(accumulated_score)

    add Solid("#120d09e8")

    frame at day_six_panel_enter:
        xalign 0.5
        yalign 0.5
        xsize 1740
        ysize 940
        padding (38, 26)
        background Solid("#261b15f8")

        vbox:
            spacing 14

            fixed:
                xsize 1664
                ysize 34
                text "REVIEW RUN  •  CHALLENGE [question_number]/5  •  EVIDENCE SCAN" size 20 bold True color "#f472b6"
                text "SKOR [day_6_review_score]/50  •  BENAR BERUNTUN: [day_6_review_streak]" xalign 1.0 size 20 bold True color "#fde68a"

            fixed:
                xsize 1664
                ysize 10
                add Solid("#4b3a31") xsize 1664 ysize 10
                add Solid("#f472b6") xsize int(1664 * question_number / 5.0) ysize 10

            hbox:
                spacing 24

                frame:
                    xsize 790
                    ysize 790
                    padding (32, 28)
                    background Solid("#f6efe3")

                    vbox:
                        spacing 20
                        text passage_title size 24 bold True color "#7c2d12" substitute False
                        add Solid("#d6b98b") xsize 726 ysize 2
                        text passage:
                            xsize 726
                            size 27
                            color "#2f241e"
                            line_spacing 10
                            substitute False

                frame:
                    xsize 850
                    ysize 790
                    padding (30, 26)
                    background Solid("#33231b")

                    vbox:
                        spacing 16
                        text "READING  •  MAIN IDEA" size 18 bold True color "#f9a8d4"
                        text prompt xsize 790 size 29 bold True color "#fff7ed" line_spacing 5 substitute False

                        if day == 7 and hint_text and hint_level > 0:
                            textbutton ("SEMBUNYIKAN PETUNJUK" if hint_visible else "BUKA PETUNJUK"):
                                xalign 1.0
                                xsize 280
                                ysize 48
                                background Solid("#59354a")
                                hover_background Solid("#831843")
                                text_color "#fce7f3"
                                text_size 18
                                action SetScreenVariable("hint_visible", not hint_visible)

                            if hint_visible:
                                text hint_text xsize 790 size 20 color "#fbcfe8" substitute False
                        elif day == 7 and hint_text:
                            text "HINT TERKUNCI • Raih minimal 30 poin dari akumulasi hari sebelumnya." xsize 790 size 17 color "#cbd5e1"

                        add Solid("#6b4d3f") xsize 790 ysize 2

                        button:
                            xfill True
                            ysize 135
                            padding (22, 15)
                            background Solid("#493229")
                            hover_background Solid("#7c4a2d")
                            action Return("a")
                            text ("A.  " + option_a) xsize 735 yalign 0.5 size 22 color "#fff7ed" substitute False

                        button:
                            xfill True
                            ysize 135
                            padding (22, 15)
                            background Solid("#493229")
                            hover_background Solid("#7c4a2d")
                            action Return("b")
                            text ("B.  " + option_b) xsize 735 yalign 0.5 size 22 color "#fff7ed" substitute False

                        button:
                            xfill True
                            ysize 135
                            padding (22, 15)
                            background Solid("#493229")
                            hover_background Solid("#7c4a2d")
                            action Return("c")
                            text ("C.  " + option_c) xsize 735 yalign 0.5 size 22 color "#fff7ed" substitute False


screen day_six_listening_challenge(question_number, audio_file, prompt, option_a, option_b, option_c):
    modal True
    zorder 110
    default replay_count = 0
    default audio_started = False

    $ audio_finished = audio_started and not renpy.music.is_playing(channel="listening")

    on "show" action [
        Stop("listening"),
        Play("listening", audio_file, loop=False),
        SetScreenVariable("audio_started", True),
    ]
    on "hide" action Stop("listening")
    on "replaced" action Stop("listening")
    key "game_menu" action NullAction()

    timer 0.10 repeat True action Function(renpy.restart_interaction)

    add Solid("#120d09e8")

    frame at day_six_panel_enter:
        xalign 0.5
        yalign 0.5
        xsize 1700
        ysize 900
        padding (40, 34)
        background Solid("#261b15f8")

        vbox:
            spacing 18

            fixed:
                xsize 1620
                ysize 34
                text "REVIEW RUN  •  CHALLENGE [question_number]/5  •  AUDIO RECALL" size 20 bold True color "#60a5fa"
                text "SKOR [day_6_review_score]/50  •  BENAR BERUNTUN: [day_6_review_streak]" xalign 1.0 size 20 bold True color "#fde68a"

            fixed:
                xsize 1620
                ysize 10
                add Solid("#4b3a31") xsize 1620 ysize 10
                add Solid("#60a5fa") xsize int(1620 * question_number / 5.0) ysize 10

            hbox:
                spacing 28

                frame:
                    xsize 560
                    ysize 750
                    padding (32, 28)
                    background Solid("#203342")

                    vbox:
                        xfill True
                        spacing 20
                        text "REKAMAN HARI 4  •  REVIEW ULANG" xalign 0.5 text_align 0.5 size 21 bold True color "#bfdbfe"
                        add Solid("#40627a") xsize 496 ysize 2
                        null height 24

                        frame:
                            xalign 0.5
                            xsize 180
                            ysize 180
                            padding (0, 0)
                            background Solid("#2563eb")
                            text "♫" xalign 0.5 yalign 0.5 size 88 bold True color "#eff6ff"

                        if not audio_finished:
                            text "AUDIO SEDANG DIPUTAR" xalign 0.5 size 23 bold True color "#93c5fd"
                        elif replay_count == 0:
                            text "SELESAI  •  REPLAY TERSEDIA" xalign 0.5 size 21 bold True color "#a7f3d0"
                        else:
                            text "SELESAI  •  REPLAY TERPAKAI" xalign 0.5 size 21 bold True color "#f8fafc"

                        bar:
                            value AudioPositionValue(channel="listening", update_interval=0.05)
                            xfill True
                            ysize 16
                            left_bar Solid("#60a5fa")
                            right_bar Solid("#475569")

                        textbutton "PUTAR ULANG  •  MAKS. 1×":
                            xalign 0.5
                            xsize 410
                            ysize 68
                            padding (22, 14)
                            background Solid("#1d4ed8")
                            hover_background Solid("#2563eb")
                            insensitive_background Solid("#334155")
                            text_color "#eff6ff"
                            text_insensitive_color "#64748b"
                            text_size 21
                            sensitive audio_finished and replay_count < 1
                            action [
                                SetScreenVariable("audio_started", False),
                                SetScreenVariable("replay_count", replay_count + 1),
                                Play("listening", audio_file, loop=False),
                                SetScreenVariable("audio_started", True),
                            ]

                        text "Pilihan terbuka setelah audio selesai. Fokus pada suggestion dan respons terakhir.":
                            xalign 0.5
                            text_align 0.5
                            xsize 490
                            size 19
                            color "#cbd5e1"

                frame:
                    xsize 1032
                    ysize 750
                    padding (32, 28)
                    background Solid("#33231b")

                    vbox:
                        spacing 17
                        text "LISTENING  •  NEXT ACTION" size 18 bold True color "#93c5fd"
                        text prompt xsize 968 size 30 bold True color "#fff7ed" line_spacing 5 substitute False
                        add Solid("#6b4d3f") xsize 968 ysize 2

                        button:
                            xfill True
                            ysize 132
                            padding (24, 17)
                            background Solid("#493229")
                            hover_background Solid("#7c4a2d")
                            insensitive_background Solid("#312b29")
                            sensitive audio_finished
                            action [Stop("listening"), Return("a")]
                            text ("A.  " + option_a) xsize 910 yalign 0.5 size 24 color ("#fff7ed" if audio_finished else "#78716c") substitute False

                        button:
                            xfill True
                            ysize 132
                            padding (24, 17)
                            background Solid("#493229")
                            hover_background Solid("#7c4a2d")
                            insensitive_background Solid("#312b29")
                            sensitive audio_finished
                            action [Stop("listening"), Return("b")]
                            text ("B.  " + option_b) xsize 910 yalign 0.5 size 24 color ("#fff7ed" if audio_finished else "#78716c") substitute False

                        button:
                            xfill True
                            ysize 132
                            padding (24, 17)
                            background Solid("#493229")
                            hover_background Solid("#7c4a2d")
                            insensitive_background Solid("#312b29")
                            sensitive audio_finished
                            action [Stop("listening"), Return("c")]
                            text ("C.  " + option_c) xsize 910 yalign 0.5 size 24 color ("#fff7ed" if audio_finished else "#78716c") substitute False

                        if not audio_finished:
                            text "Dengarkan sampai selesai untuk membuka pilihan." xalign 0.5 size 19 color "#fbbf24"


screen day_six_challenge_result(question_number, challenge_title, correct, explanation):
    modal True
    zorder 115

    $ result_color = "#34d399" if correct else "#fb7185"
    $ result_title = "CHALLENGE CLEAR  •  +10" if correct else "BELUM CLEAR  •  +0"

    add Solid("#120d09e8")

    frame at day_six_panel_enter:
        xalign 0.5
        yalign 0.5
        xsize 1040
        padding (48, 42)
        background Solid("#261b15f8")

        vbox:
            spacing 20
            text "CHALLENGE [question_number]/5  •  [challenge_title]" xalign 0.5 size 20 bold True color "#d6c7ba"
            text result_title xalign 0.5 size 40 bold True color result_color substitute False
            add Solid(result_color) xalign 0.5 xsize 180 ysize 4
            text "SKOR  [day_6_review_score]/50  •  BENAR BERUNTUN: [day_6_review_streak]" xalign 0.5 size 23 bold True color "#fde68a"

            frame:
                xfill True
                padding (26, 22)
                background Solid("#3b2a20")
                text explanation xsize 900 text_align 0.5 xalign 0.5 size 23 color "#fff7ed" line_spacing 5 substitute False

            textbutton "LANJUTKAN REVIEW":
                xalign 0.5
                xsize 420
                ysize 68
                background Solid("#7c4a2d")
                hover_background Solid("#9a5b36")
                text_color "#ffffff"
                text_size 22
                action Return(True)


screen day_six_readiness_choice():
    modal True
    zorder 110

    add Solid("#140f0bc7")

    frame at day_six_panel_enter:
        xalign 0.5
        yalign 0.5
        xsize 1380
        padding (48, 42)
        background Solid("#261b15f5")

        vbox:
            spacing 24
            text "SATU KALIMAT SEBELUM SIMULASI" xalign 0.5 size 19 bold True color "#fbbf24"
            text "Apa yang ingin [player_name] katakan?" xalign 0.5 size 38 bold True color "#fff7ed"

            textbutton "Peralatan dan alarm sudah siap. Besok aku datang tepat waktu.":
                xfill True
                ysize 86
                padding (26, 18)
                background Solid("#173f35")
                hover_background Solid("#166534")
                text_color "#f0fdf4"
                text_size 24
                action Return("practical")

            textbutton "Aku masih gugup, tetapi aku akan mempercayai latihan enam hari ini.":
                xfill True
                ysize 86
                padding (26, 18)
                background Solid("#153147")
                hover_background Solid("#075985")
                text_color "#f0f9ff"
                text_size 24
                action Return("honest")

            textbutton "Tolong larang Bima menyebut simulasi sebagai final boss setiap lima menit.":
                xfill True
                ysize 86
                padding (26, 18)
                background Solid("#4b2b24")
                hover_background Solid("#7c2d12")
                text_color "#fff7ed"
                text_size 24
                action Return("joke")


screen prologue_action_choice():
    modal True
    zorder 100
    add Solid("#020617aa")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        padding (38, 34)
        background Solid("#0f2338f2")
        vbox:
            spacing 24
            text "PILIHAN TINDAKAN" size 19 color "#22d3ee" xalign 0.5
            textbutton "Rencana yang bagus! Ayo kita belajar bersama!":
                xfill True
                padding (28, 22)
                background Solid("#164e63")
                hover_background Solid("#0891b2")
                text_color "#ffffff"
                text_size 25
                action Return("accept")


screen study_plan_ready():
    modal True
    zorder 100
    add Solid("#030712")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 860
        padding (42, 36)
        background Solid("#071a2ee8")
        vbox:
            spacing 16
            text "RENCANA BELAJAR 7 HARI" size 28 bold True color "#22d3ee"
            text "LEO SIAP MEMBIMBING KELOMPOK" size 18 color "#4ade80"
            null height 8
            text "• Hari Pertama: Vocabulary Dasar dan Context Clues" size 21 color "#e2e8f0"
            text "• Materi Utama: Vocabulary, Structure, Reading, dan Listening" size 21 color "#e2e8f0"
            text "• Metode: Penjelasan, Contoh, Latihan, dan Evaluasi" size 21 color "#e2e8f0"
            text "• Target Kelompok: Skor minimal [target_score]" size 21 color "#e2e8f0"
            null height 12
            bar value 100 range 100 xfill True
            textbutton "MULAI HARI PERTAMA  →":
                xalign 1.0
                padding (24, 12)
                background Solid("#0891b2")
                hover_background Solid("#06b6d4")
                text_color "#ffffff"
                action Return(True)


screen study_calendar_actions(review_label):
    hbox:
        xalign 0.5
        ypos 900
        spacing 20

        textbutton review_label:
            xsize 270
            ysize 64
            padding (22, 12)
            background Solid("#164e63")
            hover_background Solid("#0e7490")
            text_color "#ffffff"
            text_hover_color "#cffafe"
            text_size 22
            text_bold True
            text_xalign 0.5
            action Return("review")

        textbutton "GANTI HARI":
            xsize 240
            ysize 64
            padding (22, 12)
            background Solid("#164e63")
            hover_background Solid("#0e7490")
            text_color "#ffffff"
            text_hover_color "#cffafe"
            text_size 22
            text_bold True
            text_xalign 0.5
            action Return("switch")

        textbutton "LANJUTKAN  →":
            xsize 240
            ysize 64
            padding (22, 12)
            background Solid("#0891b2")
            hover_background Solid("#06b6d4")
            text_color "#ffffff"
            text_hover_color "#ecfeff"
            text_size 22
            text_bold True
            text_xalign 0.5
            action Return("next")


screen study_calendar_day_card(day_number, day_title, day_detail, card_state="future"):
    $ is_skipped = card_state in ("skipped", "skipped_static")
    $ paper_color = "#fff7ed" if is_skipped else ("#ecfeff" if card_state == "active" else "#f8fafc")
    $ header_color = "#d97706" if is_skipped else ("#0891b2" if card_state == "active" else ("#475569" if card_state in ("complete", "complete_static") else "#1e293b"))
    $ number_color = "#ffffff"
    $ title_color = "#b45309" if is_skipped else ("#0e7490" if card_state == "active" else "#172033")

    fixed:
        xsize 300
        ysize 380

        add Solid("#00000066") xpos 8 ypos 10 xsize 292 ysize 360

        frame:
            xsize 292
            ysize 360
            padding (0, 0)
            background Solid(paper_color)

            vbox:
                spacing 0

                frame:
                    xfill True
                    ysize 88
                    padding (0, 0)
                    background Solid(header_color)

                    text "HARI [day_number]":
                        xalign 0.5
                        yalign 0.5
                        size 30
                        bold True
                        color number_color

                frame:
                    xfill True
                    ysize 272
                    padding (24, 26)
                    background Solid(paper_color)

                    vbox:
                        xalign 0.5
                        spacing 18

                        text "[day_title]" size 31 bold True color title_color xalign 0.5
                        add Solid("#cbd5e1") xalign 0.5 xsize 190 ysize 3
                        text "[day_detail]" size 20 color "#475569" xalign 0.5 text_align 0.5 xsize 230

        if card_state == "complete":
            fixed at calendar_complete_stamp:
                xsize 292
                ysize 360

                add Transform(Solid("#e11d48"), xysize=(225, 11), rotate=-12) xalign 0.5 yalign 0.55
                add Transform(Solid("#e11d48"), xysize=(225, 11), rotate=12) xalign 0.5 yalign 0.55
                text "SELESAI" size 25 bold True color "#be123c" xalign 0.5 yalign 0.76 outlines [(2, "#ffffff", 0, 0)]

        elif card_state == "complete_static":
            fixed:
                xsize 292
                ysize 360

                add Transform(Solid("#e11d48"), xysize=(225, 11), rotate=-12) xalign 0.5 yalign 0.55
                add Transform(Solid("#e11d48"), xysize=(225, 11), rotate=12) xalign 0.5 yalign 0.55
                text "SELESAI" size 25 bold True color "#be123c" xalign 0.5 yalign 0.76 outlines [(2, "#ffffff", 0, 0)]

        elif card_state == "skipped":
            frame at calendar_complete_stamp:
                xalign 0.5
                ypos 310
                padding (20, 8)
                background Solid("#f59e0b")
                text "DILEWATI" size 19 bold True color "#ffffff"

        elif card_state == "skipped_static":
            frame:
                xalign 0.5
                ypos 310
                padding (20, 8)
                background Solid("#f59e0b")
                text "DILEWATI" size 19 bold True color "#ffffff"

        if card_state == "active":
            frame at calendar_active_badge:
                xalign 0.5
                ypos 318
                padding (22, 8)
                background Solid("#06b6d4")
                text "MULAI" size 18 bold True color "#ffffff"


screen study_calendar_transition():
    modal True
    zorder 200

    add Solid("#020617")
    add Solid("#083344") alpha 0.48

    fixed at calendar_scene_fade:
        xfill True
        yfill True

        add Solid("#22d3ee22") xpos 0 ypos 104 xsize 1920 ysize 2
        add Solid("#22d3ee16") xpos 0 ypos 884 xsize 1920 ysize 2

        text "KALENDER BELAJAR 7 HARI" xpos 960 ypos 62 xanchor 0.5 size 26 bold True color "#67e8f9"

        text "HARI 0  •  PROLOG" at calendar_old_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color "#f8fafc"

        text "HARI 1  •  VOCABULARY DASAR" at calendar_new_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color "#22d3ee"

        frame:
            xpos 140
            ypos 205
            xsize 1640
            ysize 625
            padding (0, 0)
            background Solid("#0f172af2")

            fixed:
                xsize 1640
                ysize 625

                text "RENCANA MATERI" xpos 55 ypos 28 size 18 bold True color "#94a3b8"
                text "Target: TOEFL 400+" xpos 1585 ypos 28 xanchor 1.0 size 18 color "#94a3b8"

                fixed:
                    xpos 50
                    ypos 72
                    xsize 1540
                    ysize 400
                    clipping True

                    hbox at calendar_strip_shift:
                        xpos 620
                        ypos 10
                        spacing 28

                        use study_calendar_day_card(0, "PROLOG", "Pertemuan di kantin dan pembentukan kelompok belajar.", "complete")
                        use study_calendar_day_card(1, "VOCABULARY", "Kosakata dasar dan petunjuk konteks.", "active")
                        use study_calendar_day_card(2, "STRUCTURE", "Subjek, verba, dan pola kalimat dasar.")
                        use study_calendar_day_card(3, "READING", "Ide pokok, detail, dan kosakata.")
                        use study_calendar_day_card(4, "LISTENING", "Percakapan pendek dan informasi penting.")
                        use study_calendar_day_card(5, "STRUCTURE", "Latihan pola kalimat lanjutan.")
                        use study_calendar_day_card(6, "REVIEW", "Review Reading, Listening, dan Structure.")
                        use study_calendar_day_card(7, "SIMULASI", "Ujian akhir dan evaluasi skor.")

                text "PROGRES BELAJAR" xpos 370 ypos 505 size 17 bold True color "#94a3b8"
                text "1 / 7 HARI" xpos 1270 ypos 505 xanchor 1.0 size 17 bold True color "#67e8f9"
                add Solid("#334155") xpos 370 ypos 548 xsize 900 ysize 10
                add Solid("#22d3ee") at calendar_progress_fill xpos 370 ypos 548 xsize 129 ysize 10

    use study_calendar_actions("REVIEW PROLOG")


screen study_calendar_day_one_to_two(skipped=False):
    modal True
    zorder 200

    $ day_one_result = "DILEWATI" if skipped else "SELESAI"

    add Solid("#020617")
    add Solid("#083344") alpha 0.48

    fixed at calendar_scene_fade:
        xfill True
        yfill True

        add Solid("#22d3ee22") xpos 0 ypos 104 xsize 1920 ysize 2
        add Solid("#22d3ee16") xpos 0 ypos 884 xsize 1920 ysize 2

        text "KALENDER BELAJAR 7 HARI" xpos 960 ypos 62 xanchor 0.5 size 26 bold True color "#67e8f9"

        text "HARI 1  •  VOCABULARY  •  [day_one_result]" at calendar_old_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color ("#fbbf24" if skipped else "#f8fafc")

        text "HARI 2  •  STRUCTURE DASAR" at calendar_new_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color "#22d3ee"

        frame:
            xpos 140
            ypos 205
            xsize 1640
            ysize 625
            padding (0, 0)
            background Solid("#0f172af2")

            fixed:
                xsize 1640
                ysize 625

                text "RENCANA MATERI" xpos 55 ypos 28 size 18 bold True color "#94a3b8"
                text "Target: TOEFL 400+" xpos 1585 ypos 28 xanchor 1.0 size 18 color "#94a3b8"

                fixed:
                    xpos 50
                    ypos 72
                    xsize 1540
                    ysize 400
                    clipping True

                    hbox at calendar_strip_shift:
                        xpos 292
                        ypos 10
                        spacing 28

                        use study_calendar_day_card(0, "PROLOG", "Pertemuan di kantin dan pembentukan kelompok belajar.", "complete_static")
                        use study_calendar_day_card(1, "VOCABULARY", "Kosakata dasar dan petunjuk konteks.", ("skipped" if skipped else "complete"))
                        use study_calendar_day_card(2, "STRUCTURE", "Subjek, verba, dan pola kalimat dasar.", "active")
                        use study_calendar_day_card(3, "READING", "Ide pokok, detail, dan kosakata.")
                        use study_calendar_day_card(4, "LISTENING", "Percakapan pendek dan informasi penting.")
                        use study_calendar_day_card(5, "STRUCTURE", "Latihan pola kalimat lanjutan.")
                        use study_calendar_day_card(6, "REVIEW", "Review Reading, Listening, dan Structure.")
                        use study_calendar_day_card(7, "SIMULASI", "Ujian akhir dan evaluasi skor.")

                text "PROGRES BELAJAR" xpos 370 ypos 505 size 17 bold True color "#94a3b8"
                text "2 / 7 HARI" xpos 1270 ypos 505 xanchor 1.0 size 17 bold True color "#67e8f9"
                add Solid("#334155") xpos 370 ypos 548 xsize 900 ysize 10
                add Solid("#22d3ee") at calendar_progress_day_two xpos 370 ypos 548 xsize 257 ysize 10

                if skipped:
                    text "Latihan susulan Vocabulary tersedia" xpos 820 ypos 580 xanchor 0.5 size 17 color "#fbbf24"

    use study_calendar_actions("REVIEW HARI 1")


screen study_calendar_day_two_to_three(day_one_skipped=False, day_two_skipped=False, day_one_makeup=False, day_two_makeup=False):
    modal True
    zorder 200

    $ day_two_result = "DILEWATI" if day_two_skipped else "SELESAI"
    $ makeup_note = "Latihan susulan Vocabulary dan Structure masih tersedia" if day_one_makeup and day_two_makeup else ("Latihan susulan Vocabulary masih tersedia" if day_one_makeup else ("Latihan susulan Structure masih tersedia" if day_two_makeup else ""))

    add Solid("#020617")
    add Solid("#083344") alpha 0.48

    fixed at calendar_scene_fade:
        xfill True
        yfill True

        add Solid("#22d3ee22") xpos 0 ypos 104 xsize 1920 ysize 2
        add Solid("#22d3ee16") xpos 0 ypos 884 xsize 1920 ysize 2

        text "KALENDER BELAJAR 7 HARI" xpos 960 ypos 62 xanchor 0.5 size 26 bold True color "#67e8f9"

        text "HARI 2  •  STRUCTURE  •  [day_two_result]" at calendar_old_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color ("#fbbf24" if day_two_skipped else "#f8fafc")

        text "HARI 3  •  READING DASAR" at calendar_new_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color "#22d3ee"

        frame:
            xpos 140
            ypos 205
            xsize 1640
            ysize 625
            padding (0, 0)
            background Solid("#0f172af2")

            fixed:
                xsize 1640
                ysize 625

                text "RENCANA MATERI" xpos 55 ypos 28 size 18 bold True color "#94a3b8"
                text "Target: TOEFL 400+" xpos 1585 ypos 28 xanchor 1.0 size 18 color "#94a3b8"

                fixed:
                    xpos 50
                    ypos 72
                    xsize 1540
                    ysize 400
                    clipping True

                    hbox at calendar_strip_shift:
                        xpos -36
                        ypos 10
                        spacing 28

                        use study_calendar_day_card(0, "PROLOG", "Pertemuan di kantin dan pembentukan kelompok belajar.", "complete_static")
                        use study_calendar_day_card(1, "VOCABULARY", "Kosakata dasar dan petunjuk konteks.", ("skipped_static" if day_one_skipped else "complete_static"))
                        use study_calendar_day_card(2, "STRUCTURE", "Subjek, verba, dan pola kalimat dasar.", ("skipped" if day_two_skipped else "complete"))
                        use study_calendar_day_card(3, "READING", "Ide pokok, detail, dan kosakata.", "active")
                        use study_calendar_day_card(4, "LISTENING", "Percakapan pendek dan informasi penting.")
                        use study_calendar_day_card(5, "STRUCTURE", "Latihan pola kalimat lanjutan.")
                        use study_calendar_day_card(6, "REVIEW", "Review Reading, Listening, dan Structure.")
                        use study_calendar_day_card(7, "SIMULASI", "Ujian akhir dan evaluasi skor.")

                text "PROGRES BELAJAR" xpos 370 ypos 505 size 17 bold True color "#94a3b8"
                text "3 / 7 HARI" xpos 1270 ypos 505 xanchor 1.0 size 17 bold True color "#67e8f9"
                add Solid("#334155") xpos 370 ypos 548 xsize 900 ysize 10
                add Solid("#22d3ee") at calendar_progress_day_three xpos 370 ypos 548 xsize 386 ysize 10

                if makeup_note:
                    text makeup_note xpos 820 ypos 580 xanchor 0.5 size 17 color "#fbbf24"

    use study_calendar_actions("REVIEW HARI 2")


screen study_calendar_day_three_to_four(day_one_skipped=False, day_two_skipped=False, day_three_skipped=False, day_one_makeup=False, day_two_makeup=False, day_three_makeup=False):
    modal True
    zorder 200

    $ day_three_result = "DILEWATI" if day_three_skipped else "SELESAI"
    $ pending_materials = [name for name, pending in (("Vocabulary", day_one_makeup), ("Structure", day_two_makeup), ("Reading", day_three_makeup)) if pending]
    $ makeup_note = "Latihan susulan: " + ", ".join(pending_materials) if pending_materials else ""

    add Solid("#020617")
    add Solid("#083344") alpha 0.48

    fixed at calendar_scene_fade:
        xfill True
        yfill True

        add Solid("#22d3ee22") xpos 0 ypos 104 xsize 1920 ysize 2
        add Solid("#22d3ee16") xpos 0 ypos 884 xsize 1920 ysize 2

        text "KALENDER BELAJAR 7 HARI" xpos 960 ypos 62 xanchor 0.5 size 26 bold True color "#67e8f9"

        text "HARI 3  •  READING  •  [day_three_result]" at calendar_old_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color ("#fbbf24" if day_three_skipped else "#f8fafc")

        text "HARI 4  •  LISTENING DASAR" at calendar_new_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color "#22d3ee"

        frame:
            xpos 140
            ypos 205
            xsize 1640
            ysize 625
            padding (0, 0)
            background Solid("#0f172af2")

            fixed:
                xsize 1640
                ysize 625

                text "RENCANA MATERI" xpos 55 ypos 28 size 18 bold True color "#94a3b8"
                text "Target: TOEFL 400+" xpos 1585 ypos 28 xanchor 1.0 size 18 color "#94a3b8"

                fixed:
                    xpos 50
                    ypos 72
                    xsize 1540
                    ysize 400
                    clipping True

                    hbox at calendar_strip_shift:
                        xpos -364
                        ypos 10
                        spacing 28

                        use study_calendar_day_card(0, "PROLOG", "Pertemuan di kantin dan pembentukan kelompok belajar.", "complete_static")
                        use study_calendar_day_card(1, "VOCABULARY", "Kosakata dasar dan petunjuk konteks.", ("skipped_static" if day_one_skipped else "complete_static"))
                        use study_calendar_day_card(2, "STRUCTURE", "Subjek, verba, dan pola kalimat dasar.", ("skipped_static" if day_two_skipped else "complete_static"))
                        use study_calendar_day_card(3, "READING", "Ide pokok, detail, dan kosakata.", ("skipped" if day_three_skipped else "complete"))
                        use study_calendar_day_card(4, "LISTENING", "Percakapan pendek dan informasi penting.", "active")
                        use study_calendar_day_card(5, "STRUCTURE", "Latihan pola kalimat lanjutan.")
                        use study_calendar_day_card(6, "REVIEW", "Review Reading, Listening, dan Structure.")
                        use study_calendar_day_card(7, "SIMULASI", "Ujian akhir dan evaluasi skor.")

                text "PROGRES BELAJAR" xpos 370 ypos 505 size 17 bold True color "#94a3b8"
                text "4 / 7 HARI" xpos 1270 ypos 505 xanchor 1.0 size 17 bold True color "#67e8f9"
                add Solid("#334155") xpos 370 ypos 548 xsize 900 ysize 10
                add Solid("#22d3ee") at calendar_progress_day_four xpos 370 ypos 548 xsize 514 ysize 10

                if makeup_note:
                    text makeup_note xpos 820 ypos 580 xanchor 0.5 size 17 color "#fbbf24"

    use study_calendar_actions("REVIEW HARI 3")


# Perpindahan kalender setelah seluruh alur Hari 4 selesai.
screen study_calendar_day_four_to_five(day_one_skipped=False, day_two_skipped=False, day_three_skipped=False, day_four_skipped=False, day_one_makeup=False, day_two_makeup=False, day_three_makeup=False, day_four_makeup=False):
    modal True
    zorder 200

    $ day_four_result = "DILEWATI" if day_four_skipped else "SELESAI"
    $ pending_materials = [name for name, pending in (("Vocabulary", day_one_makeup), ("Structure Dasar", day_two_makeup), ("Reading", day_three_makeup), ("Listening", day_four_makeup)) if pending]
    $ makeup_note = "Latihan susulan: " + ", ".join(pending_materials) if pending_materials else ""

    add Solid("#020617")
    add Solid("#083344") alpha 0.48

    fixed at calendar_scene_fade:
        xfill True
        yfill True

        add Solid("#22d3ee22") xpos 0 ypos 104 xsize 1920 ysize 2
        add Solid("#22d3ee16") xpos 0 ypos 884 xsize 1920 ysize 2

        text "KALENDER BELAJAR 7 HARI" xpos 960 ypos 62 xanchor 0.5 size 26 bold True color "#67e8f9"

        text "HARI 4  •  LISTENING  •  [day_four_result]" at calendar_old_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color ("#fbbf24" if day_four_skipped else "#f8fafc")

        text "HARI 5  •  STRUCTURE LANJUTAN" at calendar_new_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color "#22d3ee"

        frame:
            xpos 140
            ypos 205
            xsize 1640
            ysize 625
            padding (0, 0)
            background Solid("#0f172af2")

            fixed:
                xsize 1640
                ysize 625

                text "RENCANA MATERI" xpos 55 ypos 28 size 18 bold True color "#94a3b8"
                text "Target: TOEFL 400+" xpos 1585 ypos 28 xanchor 1.0 size 18 color "#94a3b8"

                fixed:
                    xpos 50
                    ypos 72
                    xsize 1540
                    ysize 400
                    clipping True

                    hbox at calendar_strip_shift:
                        xpos -692
                        ypos 10
                        spacing 28

                        use study_calendar_day_card(0, "PROLOG", "Pertemuan di kantin dan pembentukan kelompok belajar.", "complete_static")
                        use study_calendar_day_card(1, "VOCABULARY", "Kosakata dasar dan petunjuk konteks.", ("skipped_static" if day_one_skipped else "complete_static"))
                        use study_calendar_day_card(2, "STRUCTURE", "Subjek, verba, dan pola kalimat dasar.", ("skipped_static" if day_two_skipped else "complete_static"))
                        use study_calendar_day_card(3, "READING", "Ide pokok, detail, dan kosakata.", ("skipped_static" if day_three_skipped else "complete_static"))
                        use study_calendar_day_card(4, "LISTENING", "Percakapan pendek dan informasi penting.", ("skipped" if day_four_skipped else "complete"))
                        use study_calendar_day_card(5, "STRUCTURE", "Parallel structure dan reduced clauses.", "active")
                        use study_calendar_day_card(6, "REVIEW", "Review Reading, Listening, dan Structure.")
                        use study_calendar_day_card(7, "SIMULASI", "Ujian akhir dan evaluasi skor.")

                text "PROGRES BELAJAR" xpos 370 ypos 505 size 17 bold True color "#94a3b8"
                text "5 / 7 HARI" xpos 1270 ypos 505 xanchor 1.0 size 17 bold True color "#67e8f9"
                add Solid("#334155") xpos 370 ypos 548 xsize 900 ysize 10
                add Solid("#22d3ee") at calendar_progress_day_five xpos 370 ypos 548 xsize 643 ysize 10

                if makeup_note:
                    text makeup_note xpos 820 ypos 580 xanchor 0.5 size 17 color "#fbbf24"

    use study_calendar_actions("REVIEW HARI 4")


# Perpindahan kalender setelah seluruh alur Hari 5 selesai.
screen study_calendar_day_five_to_six(day_one_skipped=False, day_two_skipped=False, day_three_skipped=False, day_four_skipped=False, day_five_skipped=False, day_one_makeup=False, day_two_makeup=False, day_three_makeup=False, day_four_makeup=False, day_five_makeup=False):
    modal True
    zorder 200

    $ day_five_result = "DILEWATI" if day_five_skipped else "SELESAI"
    $ pending_materials = [name for name, pending in (("Vocabulary", day_one_makeup), ("Structure Dasar", day_two_makeup), ("Reading", day_three_makeup), ("Listening", day_four_makeup), ("Structure Lanjutan", day_five_makeup)) if pending]
    $ makeup_note = "Latihan susulan: " + ", ".join(pending_materials) if pending_materials else ""

    add Solid("#020617")
    add Solid("#083344") alpha 0.48

    fixed at calendar_scene_fade:
        xfill True
        yfill True

        add Solid("#22d3ee22") xpos 0 ypos 104 xsize 1920 ysize 2
        add Solid("#22d3ee16") xpos 0 ypos 884 xsize 1920 ysize 2

        text "KALENDER BELAJAR 7 HARI" xpos 960 ypos 62 xanchor 0.5 size 26 bold True color "#67e8f9"

        text "HARI 5  •  STRUCTURE LANJUTAN  •  [day_five_result]" at calendar_old_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color ("#fbbf24" if day_five_skipped else "#f8fafc")

        text "HARI 6  •  REVIEW TERPADU" at calendar_new_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color "#22d3ee"

        frame:
            xpos 140
            ypos 205
            xsize 1640
            ysize 625
            padding (0, 0)
            background Solid("#0f172af2")

            fixed:
                xsize 1640
                ysize 625

                text "RENCANA MATERI" xpos 55 ypos 28 size 18 bold True color "#94a3b8"
                text "Target: TOEFL 400+" xpos 1585 ypos 28 xanchor 1.0 size 18 color "#94a3b8"

                fixed:
                    xpos 50
                    ypos 72
                    xsize 1540
                    ysize 400
                    clipping True

                    hbox at calendar_strip_shift:
                        xpos -1020
                        ypos 10
                        spacing 28

                        use study_calendar_day_card(0, "PROLOG", "Pertemuan di kantin dan pembentukan kelompok belajar.", "complete_static")
                        use study_calendar_day_card(1, "VOCABULARY", "Kosakata dasar dan petunjuk konteks.", ("skipped_static" if day_one_skipped else "complete_static"))
                        use study_calendar_day_card(2, "STRUCTURE", "Subjek, verba, dan pola kalimat dasar.", ("skipped_static" if day_two_skipped else "complete_static"))
                        use study_calendar_day_card(3, "READING", "Ide pokok, detail, dan kosakata.", ("skipped_static" if day_three_skipped else "complete_static"))
                        use study_calendar_day_card(4, "LISTENING", "Percakapan pendek dan informasi penting.", ("skipped_static" if day_four_skipped else "complete_static"))
                        use study_calendar_day_card(5, "STRUCTURE", "Parallel structure dan reduced clauses.", ("skipped" if day_five_skipped else "complete"))
                        use study_calendar_day_card(6, "REVIEW TERPADU", "Review Vocabulary, Structure, Reading, dan Listening.", "active")
                        use study_calendar_day_card(7, "SIMULASI", "Ujian akhir dan evaluasi skor.")

                text "PROGRES BELAJAR" xpos 370 ypos 505 size 17 bold True color "#94a3b8"
                text "6 / 7 HARI" xpos 1270 ypos 505 xanchor 1.0 size 17 bold True color "#67e8f9"
                add Solid("#334155") xpos 370 ypos 548 xsize 900 ysize 10
                add Solid("#22d3ee") at calendar_progress_day_six xpos 370 ypos 548 xsize 771 ysize 10

                if makeup_note:
                    text makeup_note xpos 820 ypos 580 xanchor 0.5 xsize 1500 text_align 0.5 size 17 color "#fbbf24"

    use study_calendar_actions("REVIEW HARI 5")


# Perpindahan kalender setelah Review Terpadu Hari 6 selesai.
screen study_calendar_day_six_to_seven(day_one_skipped=False, day_two_skipped=False, day_three_skipped=False, day_four_skipped=False, day_five_skipped=False, day_six_skipped=False, day_one_makeup=False, day_two_makeup=False, day_three_makeup=False, day_four_makeup=False, day_five_makeup=False, day_six_makeup=False):
    modal True
    zorder 200

    $ day_six_result = "DILEWATI" if day_six_skipped else "SELESAI"
    $ pending_materials = [name for name, pending in (("Vocabulary", day_one_makeup), ("Structure Dasar", day_two_makeup), ("Reading", day_three_makeup), ("Listening", day_four_makeup), ("Structure Lanjutan", day_five_makeup), ("Review Terpadu", day_six_makeup)) if pending]
    $ makeup_note = "Latihan susulan: " + ", ".join(pending_materials) if pending_materials else ""

    add Solid("#020617")
    add Solid("#083344") alpha 0.48

    fixed at calendar_scene_fade:
        xfill True
        yfill True

        add Solid("#22d3ee22") xpos 0 ypos 104 xsize 1920 ysize 2
        add Solid("#22d3ee16") xpos 0 ypos 884 xsize 1920 ysize 2

        text "KALENDER BELAJAR 7 HARI" xpos 960 ypos 62 xanchor 0.5 size 26 bold True color "#67e8f9"

        text "HARI 6  •  REVIEW TERPADU  •  [day_six_result]" at calendar_old_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color ("#fbbf24" if day_six_skipped else "#f8fafc")

        text "HARI 7  •  SIMULASI AKHIR" at calendar_new_caption:
            xpos 960
            ypos 121
            xanchor 0.5
            size 43
            bold True
            color "#22d3ee"

        frame:
            xpos 140
            ypos 205
            xsize 1640
            ysize 625
            padding (0, 0)
            background Solid("#0f172af2")

            fixed:
                xsize 1640
                ysize 625

                text "RENCANA MATERI" xpos 55 ypos 28 size 18 bold True color "#94a3b8"
                text "Target: TOEFL 400+" xpos 1585 ypos 28 xanchor 1.0 size 18 color "#94a3b8"

                fixed:
                    xpos 50
                    ypos 72
                    xsize 1540
                    ysize 400
                    clipping True

                    hbox at calendar_strip_shift:
                        xpos -1348
                        ypos 10
                        spacing 28

                        use study_calendar_day_card(0, "PROLOG", "Pertemuan di kantin dan pembentukan kelompok belajar.", "complete_static")
                        use study_calendar_day_card(1, "VOCABULARY", "Kosakata dasar dan petunjuk konteks.", ("skipped_static" if day_one_skipped else "complete_static"))
                        use study_calendar_day_card(2, "STRUCTURE", "Subjek, verba, dan pola kalimat dasar.", ("skipped_static" if day_two_skipped else "complete_static"))
                        use study_calendar_day_card(3, "READING", "Ide pokok, detail, dan kosakata.", ("skipped_static" if day_three_skipped else "complete_static"))
                        use study_calendar_day_card(4, "LISTENING", "Percakapan pendek dan informasi penting.", ("skipped_static" if day_four_skipped else "complete_static"))
                        use study_calendar_day_card(5, "STRUCTURE", "Parallel structure dan reduced clauses.", ("skipped_static" if day_five_skipped else "complete_static"))
                        use study_calendar_day_card(6, "REVIEW TERPADU", "Mini-game Vocabulary, Structure, Reading, dan Listening di kafe.", ("skipped" if day_six_skipped else "complete"))
                        use study_calendar_day_card(7, "SIMULASI AKHIR", "Ujian akhir dan evaluasi skor.", "active")

                text "PROGRES BELAJAR" xpos 370 ypos 505 size 17 bold True color "#94a3b8"
                text "7 / 7 HARI" xpos 1270 ypos 505 xanchor 1.0 size 17 bold True color "#67e8f9"
                add Solid("#334155") xpos 370 ypos 548 xsize 900 ysize 10
                add Solid("#22d3ee") at calendar_progress_day_seven xpos 370 ypos 548 xsize 900 ysize 10

                if makeup_note:
                    text makeup_note xpos 820 ypos 580 xanchor 0.5 xsize 1500 text_align 0.5 size 17 color "#fbbf24"

    use study_calendar_actions("REVIEW HARI 6")


screen study_day_review(day_number):
    """Ringkasan kegiatan hari yang sudah selesai, tanpa memulai hari baru."""
    modal True
    zorder 300
    add Solid("#020617dd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 920
        ysize 560
        padding (42, 36)
        background Solid("#0f2338f5")

        vbox:
            spacing 18
            text "REVIEW KEGIATAN HARI [day_number]" size 30 bold True color "#67e8f9" xalign 0.5
            null height 4

            if day_number == 0:
                text "PROLOG — Persiapan Study Group" size 26 bold True color "#f8fafc"
                text "Pembentukan kelompok belajar, pengumuman target skor 400, dan aktivasi Kalender Belajar 7 Hari bersama Leo." size 21 color "#cbd5e1" line_spacing 6
                text "Status: selesai" size 20 color "#4ade80"
            elif day_number == 1:
                text "VOCABULARY DASAR" size 26 bold True color "#f8fafc"
                text "Kegiatan: latihan context clue, kosakata akademik, strategi mengganti kata dengan pilihan jawaban, dan latihan Vocabulary." size 21 color "#cbd5e1" line_spacing 6
                text "Skor: [day_1_vocab_score] / 50" size 20 color "#fbbf24"
            elif day_number == 2:
                text "STRUCTURE DASAR" size 26 bold True color "#f8fafc"
                text "Kegiatan: subject–verb agreement, finite verb, clause, dan pemeriksaan struktur kalimat." size 21 color "#cbd5e1" line_spacing 6
                text "Skor: [day_2_structure_score] / 50" size 20 color "#fbbf24"
            elif day_number == 3:
                text "READING DASAR" size 26 bold True color "#f8fafc"
                text "Kegiatan: main idea, supporting details, reference, vocabulary in context, dan inference." size 21 color "#cbd5e1" line_spacing 6
                text "Skor: [day_3_reading_score] / 50" size 20 color "#fbbf24"
            elif day_number == 4:
                text "LISTENING DASAR" size 26 bold True color "#f8fafc"
                text "Kegiatan: menangkap keyword, intent pembicara, suggestion, contrast, dan informasi tersirat." size 21 color "#cbd5e1" line_spacing 6
                text "Skor: [day_4_listening_score] / 50" size 20 color "#fbbf24"
            elif day_number == 5:
                text "STRUCTURE LANJUTAN" size 26 bold True color "#f8fafc"
                text "Kegiatan: parallel structure, reduced relative clause, voice, dan dangling modifier." size 21 color "#cbd5e1" line_spacing 6
                text "Skor: [day_5_structure_score] / 50" size 20 color "#fbbf24"
            elif day_number == 6:
                text "REVIEW TERPADU" size 26 bold True color "#f8fafc"
                text "Kegiatan: lima kartu review yang menggabungkan Vocabulary, Structure, Reading, dan Listening." size 21 color "#cbd5e1" line_spacing 6
                text "Skor: [day_6_review_score] / 50" size 20 color "#fbbf24"
            elif day_number == 7:
                text "SIMULASI TOEFL" size 26 bold True color "#f8fafc"
                text "Kegiatan: ujian simulasi, verifikasi identitas, dan evaluasi skor akhir bersama Study Group." size 21 color "#cbd5e1" line_spacing 6
                text "Skor ujian: [day_7_exam_score] / 600" size 20 color "#fbbf24"
                text "Total: [day_7_final_score] / 950" size 20 color "#67e8f9"
            else:
                text "REVIEW KEGIATAN" size 26 bold True color "#f8fafc"
                text "Ringkasan hari ini belum tersedia." size 21 color "#cbd5e1" line_spacing 6

            if day_number > 0:
                text "Bonus latihan tambahan tersimpan: [extra_practice_score] poin." size 18 color "#a7f3d0"

            null height 12
            textbutton "TUTUP REVIEW":
                xalign 0.5
                padding (26, 12)
                background Solid("#0891b2")
                hover_background Solid("#06b6d4")
                text_color "#ffffff"
                text_size 21
                action Return(True)


screen study_day_switcher(current_day):
    modal True
    zorder 310
    add Solid("#020617dd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 760
        padding (34, 30)
        background Solid("#0f2338f7")

        vbox:
            spacing 18
            text "GANTI HARI" size 31 bold True color "#67e8f9" xalign 0.5
            text "Hanya hari sebelumnya dan satu hari setelah Hari [current_day] yang tersedia." size 18 color "#cbd5e1" xalign 0.5 text_align 0.5

            if current_day > 0:
                textbutton "← HARI [current_day - 1]  •  REVIEW":
                    xfill True
                    padding (20, 14)
                    background Solid("#164e63")
                    hover_background Solid("#0891b2")
                    text_size 22
                    text_color "#ffffff"
                    action Return(current_day - 1)

            textbutton "HARI [current_day]  •  SEDANG AKTIF":
                xfill True
                padding (20, 14)
                background Solid("#334155")
                text_size 22
                text_color "#cbd5e1"
                sensitive False

            if current_day < 7:
                textbutton "HARI [current_day + 1]  •  MULAI SESUDAH KONFIRMASI →":
                    xfill True
                    padding (20, 14)
                    background Solid("#0b8797")
                    hover_background Solid("#06b6d4")
                    text_size 22
                    text_color "#ffffff"
                    action Return(current_day + 1)

            textbutton "BATAL":
                xalign 0.5
                padding (18, 10)
                text_size 20
                text_color "#fda4af"
                action Return("cancel")


screen study_day_switcher_all(current_day):
    """Pemilih kalender: seluruh hari yang sudah terbuka dapat dipilih."""
    modal True
    zorder 310
    add Solid("#020617dd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 820
        padding (34, 30)
        background Solid("#0f2338f7")
        vbox:
            spacing 12
            text "GANTI HARI" size 31 bold True color "#67e8f9" xalign 0.5
            text "Pilih hari yang sudah terbuka. Hari berikutnya hanya tersedia untuk dilanjutkan." size 18 color "#cbd5e1" xalign 0.5 text_align 0.5

            if current_day > 0:
                textbutton "HARI 0  •  REVIEW PROLOG":
                    xfill True
                    padding (14, 9)
                    background Solid("#164e63")
                    hover_background Solid("#0891b2")
                    text_size 18
                    text_color "#ffffff"
                    action Return(0)

            for option_day in range(1, 8):
                $ unlocked = True
                $ status_label = "HARI INI" if option_day == current_day else ("LANJUTKAN" if option_day == current_day + 1 else ("REVIEW" if option_day < current_day else "MULAI"))
                textbutton ("HARI [option_day]  •  " + status_label):
                    xfill True
                    padding (14, 9)
                    background Solid("#0b8797" if option_day == current_day + 1 else ("#164e63" if unlocked else "#1e293b"))
                    hover_background Solid("#06b6d4")
                    text_size 18
                    text_color ("#ffffff" if unlocked else "#64748b")
                    sensitive unlocked
                    action Return(option_day)

            textbutton "BATAL":
                xalign 0.5
                padding (16, 8)
                text_size 19
                text_color "#fda4af"
                action Return("cancel")


################################################################################
## Gaya
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## Layar In-game
################################################################################


## Layar Say ###################################################################
##
## Layar say di gunakan untuk menampilkan dialog kepada pemain. Ini menggunakan
## dua parameter, who dan what, yang merupakan nama karakter yang berbicara dan
## text yang akan di tampilkan, masing-masing. (Kedua parameter dapat berisi
## None jika tidak ada nama yang di berikan.
##
## Layar ini harus membuat text yang dapat di tampilkan dengan id "what", yang
## di mana Ren'Py menggunakan ini untuk mengatur tampilan text. Ini juga dapat
## membuat sesuatu yang dapat di tampilkan dengan id "who" dan id "window" untuk
## mengaplikasikan properti gaya.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## Jika ada gambar di sisi, tampilkan di atas text. Jangan tampilkan di
    ## versi HP[Handphone)(Android) - Karena tidak ada ruang.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Buat namebox tersedia untuk mengatur gaya melalui objek karakter.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Layar masukkan/input ########################################################
##
## Layar ini di gunakan untuk menampilkan renpy.input. Parameter prompt
## digunakan untuk meneruskan text yang di prompt/minta.
##
## Layar ini harus membuat input yang dapat di tampilkan dengan id "input" untuk
## menerima berbagai parameter masukan.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Layar Pilihan ###############################################################
##
## Layar ini digunakan untuk menampilkan pilihan dalam game yang disajikan oleh
## menu statement. Satu parameter, item, adalah daftar objek, masing-masing
## dengan bidang keterangan dan tindakan.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Layar Menu Cepat/Quick Menu #################################################
##
## Menu cepat ditampilkan dalam game untuk memudahkan akses ke menu di luar
## game.

screen quick_menu():

    ## Memastikan ini muncul di atas layar yang lain.
    zorder 100

    if quick_menu:

        textbutton _("☰"):
            style "quick_icon_button"
            xpos 24
            ypos 24
            action ShowMenu("navigation")

        hbox:
            style_prefix "quick"
            style "quick_menu"

            textbutton _("↩"):
                style "quick_icon_button"
                action Rollback()
            textbutton _("»"):
                style "quick_icon_button"
                action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("A"):
                style "quick_auto_button"
                action Preference("auto-forward", "toggle")


## Kode ini memastikan layar quick_menu di tampilkan di dalam permainan,
## kapanpun player tidak secaralangsung menyembunyikan antarmuka.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

style quick_icon_button is quick_button
style quick_icon_button_text is quick_button_text
style quick_auto_button is quick_icon_button
style quick_auto_button_text is quick_icon_button_text

style quick_menu:
    xalign 0.5
    yalign 1.0

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")

style quick_icon_button:
    xsize 58
    ysize 48
    padding (0, 0)
    background Solid("#062f35cc")
    hover_background Solid("#1596a8dd")

style quick_auto_button:
    selected_background Solid("#1596a8dd")

style quick_icon_button_text:
    font gui.interface_text_font
    size 28
    bold True
    color "#f8fffe"
    hover_color "#fff7c2"
    xalign 0.5
    yalign 0.5


################################################################################
## Layar Menu Utama dan Menu Permainan
################################################################################

## Layar navigasi ##############################################################

transform hover_biru_zoom:
    zoom 1.05
    matrixcolor TintMatrix("#cfe8ff") * BrightnessMatrix(0.04)


transform main_menu_title_enter:
    alpha 0.0
    yoffset -24
    easeout 0.45 alpha 1.0 yoffset 0


transform main_menu_panel_enter:
    alpha 0.0
    xoffset 70
    pause 0.1
    easeout 0.45 alpha 1.0 xoffset 0


transform main_menu_button_shift:
    on idle:
        easeout 0.12 xoffset 0
    on hover:
        easeout 0.12 xoffset -12



screen navigation():

    ## Panel latar belakang — meniru desain panel main_menu
    fixed:
        xpos 0
        ypos 0
        xsize 420
        yfill True

        add Solid("#062f35dc") xsize 420
        add Solid("#77e3e8")   xpos 414 xsize 6
        add Solid("#ffffff18") xpos 40 ypos 175 xsize 335 ysize 2

        text "NAVIGASI":
            xpos 45
            ypos 116
            font gui.interface_text_font
            size 31
            bold True
            color "#a9f3f2"

        text "Pilih menu":
            xpos 45
            ypos 149
            font gui.interface_text_font
            size 22
            color "#d7f4f2"

        textbutton _("×"):
            style "quick_icon_button"
            xpos 344
            ypos 112
            action Return()

        vbox:
            xpos 42
            ypos 212
            spacing 10

            if main_menu:

                textbutton _("01   MULAI CERITA"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action ShowMenu("story_start_screen")
                    at main_menu_button_shift

            else:

                textbutton _("01   RIWAYAT"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action ShowMenu("history")
                    at main_menu_button_shift

                textbutton _("02   SAVE"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action FileSave("story-main", confirm=False, page=1, slot=True, action=Return())
                    at main_menu_button_shift

            if main_menu:
                textbutton _("02   PENGATURAN"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action ShowMenu("preferences")
                    at main_menu_button_shift
            else:
                textbutton _("03   PENGATURAN"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action ShowMenu("preferences")
                    at main_menu_button_shift

            if main_menu:
                textbutton _("03   TENTANG GAME"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action ShowMenu("about")
                    at main_menu_button_shift
            else:
                textbutton _("04   TENTANG GAME"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action ShowMenu("about")
                    at main_menu_button_shift

            if main_menu:
                textbutton _("04   BANTUAN"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action ShowMenu("help")
                    at main_menu_button_shift
            else:
                textbutton _("05   BANTUAN"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action ShowMenu("help")
                    at main_menu_button_shift

            if not main_menu:

                textbutton _("06   MENU UTAMA"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#1596a8dd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action MainMenu()
                    at main_menu_button_shift

            if main_menu:
                textbutton _("05   KELUAR"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#c94f5ddd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action Quit(confirm=True)
                    at main_menu_button_shift
            else:
                textbutton _("07   KELUAR"):
                    xsize 340
                    ysize 68
                    padding (22, 12)
                    background Solid("#ffffff14")
                    hover_background Solid("#c94f5ddd")
                    text_font gui.interface_text_font
                    text_size 27
                    text_bold True
                    text_color "#f8fffe"
                    text_hover_color "#ffffff"
                    text_xalign 0.0
                    text_yalign 0.5
                    action Quit(confirm=True)
                    at main_menu_button_shift


screen story_start_screen():

    tag menu
    modal True
    add gui.main_menu_background
    add Solid("#071a1e9e")
    add Solid("#031d26cc") xpos 0.0 xsize 1920 ysize 1080

    $ slots = story_save_slots(1)

    vbox:
        xalign 0.5
        ypos 70
        spacing 12
        text "MULAI CERITA" size 58 bold True color "#fffdf0" xalign 0.5 outlines [(3, "#173d3c", 1, 2)]
        text "Pilih awal perjalanan atau lanjutkan salah satu catatanmu." size 23 color "#bfe8e6" xalign 0.5

    textbutton "MULAI PERMAINAN BARU  →":
        xalign 0.5
        ypos 190
        xsize 620
        ysize 82
        background Solid("#0b8797e8")
        hover_background Solid("#11b6c3")
        text_size 31
        text_bold True
        text_color "#ffffff"
        text_hover_color "#fff7c2"
        action Start()

    text "LANJUTKAN PERMAINAN" size 27 bold True color "#d7f4f2" xalign 0.5 ypos 320

    hbox:
        xalign 0.5
        ypos 375
        spacing 22

        for index, save_data in enumerate(slots):
            if save_data:
                button:
                    xsize 400
                    ysize 270
                    padding (24, 20)
                    background Solid("#0b3444e8")
                    hover_background Solid("#126579f2")
                    action FileLoad(save_data["slot"], confirm=False, slot=True)

                    hbox:
                        spacing 16

                        frame:
                            xsize 124
                            ysize 124
                            padding (4, 4)
                            background Solid("#071a1e")
                            add Transform(save_data["portrait"], crop=(340, 20, 340, 340), xysize=(116, 116))

                        vbox:
                            spacing 8
                            yalign 0.5
                            text "SAVE [index + 1]" size 19 bold True color "#7ee8ec"
                            text save_data["name"] size 27 bold True color "#ffffff"
                            text "Gender: [save_data['gender']]" size 18 color "#bfe8e6"
                            text FileTime(save_data["slot"], format="%d %b %Y, %H:%M", empty="Slot Kosong", slot=True) size 16 color "#9bc2c2"
                            text "Klik untuk melanjutkan" size 16 color "#fbbf24"
            else:
                frame:
                    xsize 400
                    ysize 270
                    padding (24, 20)
                    background Solid("#102a36c7")
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 10
                        text "SAVE [index + 1]" size 19 bold True color "#6c9798" xalign 0.5
                        text "Slot Kosong" size 29 color "#8ba5a5" xalign 0.5
                        text "Belum ada catatan permainan" size 18 color "#668083" xalign 0.5

    textbutton "← KEMBALI KE MENU UTAMA":
        xalign 0.5
        ypos 820
        padding (22, 12)
        background Solid("#ffffff16")
        hover_background Solid("#c94f5ddd")
        text_size 22
        text_color "#f8fffe"
        action [Hide("story_start_screen"), ShowMenu("main_menu")]

    key "K_ESCAPE" action [Hide("story_start_screen"), ShowMenu("main_menu")]


screen achievement_screen():
    tag menu
    modal True
    add gui.main_menu_background
    add Solid("#071a1e9e")
    add Solid("#031d26cc") xpos 0.0 xsize 1920 ysize 1080

    $ ending_defs = [
        ("ENDING S - NILAI TINGGI", "NILAI TINGGI", "Skor ujian sangat tinggi tanpa pelanggaran prosedur."),
        ("ENDING A - LULUS DI ATAS 400", "LULUS DI ATAS 400", "Target 400 tercapai melalui latihan yang konsisten."),
        ("ENDING C - TIDAK LULUS (DI BAWAH 400)", "DI BAWAH 400", "Belum mencapai target, tetapi masih bisa mengulang latihan."),
        ("ENDING X - NILAI TINGGI, TERDETEKSI CURANG", "NILAI TINGGI + CURANG", "Skor tinggi dibatalkan karena barang terlarang terlihat kamera."),
        ("ENDING Y - LULUS SKOR, TERDETEKSI CURANG", "LULUS SKOR + CURANG", "Skor melewati 400, tetapi hasil ujian tidak sah."),
        ("ENDING Z - TIDAK LULUS DAN TERDETEKSI CURANG", "DI BAWAH 400 + CURANG", "Skor rendah dan prosedur ujian juga dilanggar."),
    ]
    $ gallery = getattr(persistent, "ending_gallery", {}) or {}

    vbox:
        xalign 0.5
        ypos 55
        spacing 16
        text "PENCAPAIAN" size 55 bold True color "#fffdf0" xalign 0.5 outlines [(3, "#173d3c", 1, 2)]
        text "Koleksi ending dari setiap jalan permainan" size 22 color "#bfe8e6" xalign 0.5

        frame:
            xsize 1390
            ysize 790
            padding (24, 22)
            background Solid("#071923ee")
            vbox:
                spacing 16
                for row in range(3):
                    hbox:
                        spacing 16
                        for column in range(2):
                            $ ending_key, ending_name, ending_detail = ending_defs[row * 2 + column]
                            $ record = gallery.get(ending_key)
                            frame:
                                xsize 650
                                ysize 225
                                padding (20, 16)
                                background Solid("#124453" if record else "#102a36")
                                vbox:
                                    spacing 7
                                    text ("★  " + ending_name if record else "???  ENDING TERKUNCI") size 23 bold True color ("#fde68a" if record else "#64748b")
                                    text (ending_detail if record else "Selesaikan satu permainan untuk membuka pencapaian ini.") size 16 color ("#dbeafe" if record else "#64748b") line_spacing 3
                                    if record:
                                        text "Skor total: [record.get('score', 0)]  •  Ujian: [record.get('exam_score', 0)]" size 16 color "#a7f3d0"
                                        text "Pemain: [record.get('player_name', 'Pemain')]" size 15 color "#cbd5e1"

    textbutton "← KEMBALI KE MENU UTAMA":
        xalign 0.5
        ypos 920
        padding (22, 12)
        background Solid("#ffffff16")
        hover_background Solid("#c94f5ddd")
        text_size 22
        text_color "#f8fffe"
        action [Hide("achievement_screen"), ShowMenu("main_menu")]

    key "K_ESCAPE" action [Hide("achievement_screen"), ShowMenu("main_menu")]

## Layar Menu utama ############################################################

screen main_menu():

    tag menu

    # Gunakan ilustrasi yang menampilkan Player sesuai gender yang dipilih.
    # Saat belum ada pilihan (misalnya pertama kali membuka game), default-nya perempuan.
    add ("bg main menu night male" if player_gender == "male" else "bg main menu night female")

    # Lapisan tipis ini menjaga tulisan tetap terbaca tanpa menutupi suasana
    # ruang kelas pada gambar latar.
    add Solid("#071a1e24")
    add Solid("#02061722") xpos 0 ypos 0 xsize 1450 ysize 1080

    $ menu_completed_days = sum(int(status == "completed") for status in (day_1_status, day_2_status, day_3_status, day_4_status, day_5_status, day_6_status, day_7_status))
    $ menu_ending_count = len(getattr(persistent, "ending_gallery", {}) or {})

    frame:
        xpos 96
        ypos 118
        xsize 455
        ysize 54
        padding (18, 10)
        background Solid("#082f3dcc")
        text "STUDY GROUP  •  CAMPUS MODE" size 18 bold True color "#a7f3d0" xalign 0.5 yalign 0.5

    # Judul ditempatkan langsung pada papan tulis agar menyatu dengan tema
    # sekolah dan belajar TOEFL.
    vbox at main_menu_title_enter:
        # Geser sedikit ke kanan agar judul tidak menutupi wajah karakter.
        xpos 765
        ypos 150
        xsize 800
        spacing -8

        text "SEVEN DAYS":
            xalign 0.5
            font gui.interface_text_font
            size 78
            bold True
            color "#fffdf0"
            outlines [(3, "#173d3ccc", 1, 2)]

        text "TO TOEFL":
            xalign 0.5
            font gui.interface_text_font
            size 112
            bold True
            color "#8ee9f2"
            outlines [(4, "#173d3cee", 1, 3)]

        null height 18

        text "TUJUH HARI BELAJAR  -  SATU TARGET BESAR":
            xalign 0.5
            font gui.interface_text_font
            size 27
            color "#fff9db"
            outlines [(2, "#173d3cbb", 1, 1)]

        text "Buka catatan. Pilih strategi. Taklukkan TOEFL 400+." xalign 0.5 size 21 color "#d7f4f2"

        null height 34

        hbox:
            xalign 0.5
            spacing 15

            text "D0" size 22 color "#d7f4f2" xalign 0.5 yalign 0.5
            text "●" size 24 color "#73d9dd" xalign 0.5 yalign 0.5
            text "D1" size 22 color "#fffdf0" xalign 0.5 yalign 0.5
            text "●" size 24 color "#73d9dd" xalign 0.5 yalign 0.5
            text "D2" size 22 color "#fffdf0" xalign 0.5 yalign 0.5
            text "●" size 24 color "#73d9dd" xalign 0.5 yalign 0.5
            text "D3" size 22 color "#fffdf0" xalign 0.5 yalign 0.5
            text "●" size 24 color "#73d9dd" xalign 0.5 yalign 0.5
            text "D4" size 22 color "#fffdf0" xalign 0.5 yalign 0.5
            text "●" size 24 color "#73d9dd" xalign 0.5 yalign 0.5
            text "D5" size 22 color "#fffdf0" xalign 0.5 yalign 0.5
            text "●" size 24 color "#73d9dd" xalign 0.5 yalign 0.5
            text "D6" size 22 color "#fffdf0" xalign 0.5 yalign 0.5
            text "●" size 24 color "#73d9dd" xalign 0.5 yalign 0.5
            text "D7" size 22 color "#fffdf0" xalign 0.5 yalign 0.5

    frame:
        xpos 96
        ypos 785
        xsize 620
        ysize 205
        padding (24, 20)
        background Solid("#062f35c7")
        vbox:
            spacing 10
            text "PROGRES PERJALANAN" size 18 bold True color "#a9f3f2"
            hbox:
                xfill True
                text "HARI [menu_completed_days] / 7" size 27 bold True color "#fffdf0"
                text "[menu_ending_count] / 6 ENDING" xalign 1.0 size 18 color "#fde68a"
            bar:
                value menu_completed_days
                range 7
                xfill True
                ysize 12
                left_bar Solid("#22d3ee")
                right_bar Solid("#164e63")
            text "Setiap ending yang terbuka akan tersimpan di Pencapaian." size 16 color "#bfe8e6"

    # Panel navigasi dipasang rapat ke tepi kanan agar komposisi utama dan
    # ilustrasi meja tetap terlihat jelas.
    fixed at main_menu_panel_enter:
        xpos 1495
        ypos 0
        xsize 425
        ysize 1080

        add Solid("#062f35dc") xsize 425 ysize 1080
        add Solid("#77e3e8") xpos 0 xsize 6 ysize 1080
        add Solid("#ffffff18") xpos 38 ypos 177 xsize 330 ysize 2

        frame:
            xpos 40
            ypos 68
            xsize 340
            ysize 36
            padding (10, 5)
            background Solid("#0e7490aa")
            text "MENU UTAMA  /  [config.version]" size 15 bold True color "#cffafe" xalign 0.5 yalign 0.5

        text "MAIN MENU":
            xpos 43
            ypos 118
            font gui.interface_text_font
            size 31
            bold True
            color "#a9f3f2"

        text "Pilih langkahmu":
            xpos 43
            ypos 151
            font gui.interface_text_font
            size 22
            color "#d7f4f2"

        vbox:
            xpos 40
            ypos 220
            spacing 15

            textbutton _("01   MULAI CERITA") at main_menu_button_shift:
                xsize 340
                ysize 75
                padding (24, 15)
                background Solid("#ffffff14")
                hover_background Solid("#1596a8dd")
                text_font gui.interface_text_font
                text_size 29
                text_bold True
                text_color "#f8fffe"
                text_hover_color "#ffffff"
                text_xalign 0.0
                text_yalign 0.5
                action ShowMenu("story_start_screen")

            textbutton _("02   PENGATURAN") at main_menu_button_shift:
                xsize 340
                ysize 75
                padding (24, 15)
                background Solid("#ffffff14")
                hover_background Solid("#1596a8dd")
                text_font gui.interface_text_font
                text_size 29
                text_bold True
                text_color "#f8fffe"
                text_hover_color "#ffffff"
                text_xalign 0.0
                text_yalign 0.5
                action ShowMenu("preferences")

            textbutton _("03   PENCAPAIAN") at main_menu_button_shift:
                xsize 340
                ysize 75
                padding (24, 15)
                background Solid("#ffffff14")
                hover_background Solid("#1596a8dd")
                text_font gui.interface_text_font
                text_size 29
                text_bold True
                text_color "#f8fffe"
                text_hover_color "#ffffff"
                text_xalign 0.0
                text_yalign 0.5
                action ShowMenu("achievement_screen")

            textbutton _("04   TENTANG GAME") at main_menu_button_shift:
                xsize 340
                ysize 75
                padding (24, 15)
                background Solid("#ffffff14")
                hover_background Solid("#1596a8dd")
                text_font gui.interface_text_font
                text_size 29
                text_bold True
                text_color "#f8fffe"
                text_hover_color "#ffffff"
                text_xalign 0.0
                text_yalign 0.5
                action ShowMenu("about")

            textbutton _("05   BANTUAN") at main_menu_button_shift:
                xsize 340
                ysize 75
                padding (24, 15)
                background Solid("#ffffff14")
                hover_background Solid("#1596a8dd")
                text_font gui.interface_text_font
                text_size 29
                text_bold True
                text_color "#f8fffe"
                text_hover_color "#ffffff"
                text_xalign 0.0
                text_yalign 0.5
                action ShowMenu("help")

            textbutton _("06   KELUAR") at main_menu_button_shift:
                xsize 340
                ysize 75
                padding (24, 15)
                background Solid("#ffffff14")
                hover_background Solid("#c94f5ddd")
                text_font gui.interface_text_font
                text_size 29
                text_bold True
                text_color "#f8fffe"
                text_hover_color "#ffffff"
                text_xalign 0.0
                text_yalign 0.5
                action Quit(confirm=True)

        text "TOEFL STUDY VISUAL NOVEL":
            xpos 43
            ypos 948
            font gui.interface_text_font
            size 21
            color "#a9cfce"

        text "Versi [config.version]":
            xpos 43
            ypos 980
            font gui.interface_text_font
            size 19
            color "#7fa8a7"

## layar Menu Permainan ########################################################
##
## Ini menjalaskan struktur dasar yang paling sering di gunakan di layar menu
## permainan, ini ditampilkan beserta layar judul, dan menampilkan latar
## belakang,judul,dan navigasi.
##
## Parameter scroll dapat berisi 'None', atau "viewport" dan "vpgrid". Layar
## ini di maksudkan untuk di gunakan dengan cabang satu atau lebih, yang di
## tempatkan di dalamnya.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Memesan tempat untuk bagian navigasi.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Kembali"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 430
    ysize 180

style game_menu_label_text:
    size 65
    color "#a9f3f2"
    yalign 0.5
    font gui.interface_text_font
    bold True

style return_button:
    xpos 42
    yalign 1.0
    yoffset -45
    xsize 340
    ysize 58
    padding (22, 10)
    background Solid("#ffffff14")
    hover_background Solid("#1596a8dd")

style return_button_text:
    font gui.interface_text_font
    size 25
    bold True
    color "#a9f3f2"
    hover_color "#ffffff"
    xalign 0.0
    yalign 0.5


## Layar About #################################################################
##
## Layar ini menampilkan credit dan informasi copyright tentang game dan Ren.Py.
##
## Tidak ada yang spesial dengan layar ini, semenjak ini juga berperan sebagai
## contoh bagaimana membuat layar custom.

screen about():

    tag menu

    ## Pernyataan 'use' ini mengikutsertakan layar game_menu ke dalam layar ini.
    ## Percabangan vbox lalu di ikutsertakan kedalam viewport di dalam layar
    ## game_menu.
    use game_menu(_("Tentang"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Versi [config.version!t]\n")

            ## gui.about biasanya di set di options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Dibuat Dengan {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Layar Load and Save #########################################################
##
## Layar ini bertanggungjawab untuk mengijinkan pemain menyimpan dan
## meload lagi. Semenjak mereke hampir memiliki hal yang sama, keduanya di
## implementasinan di percabangan layar ketiga, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Simpan"))


screen load():

    tag menu

    use file_slots(_("Muat"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Halaman {}"), auto=_("Otomatis save"), quick=_("Save cepat"))

    use game_menu(title):

        fixed:

            ## Ini memastikan input akan mendapat event masuk sebelum tombol
            ## lainnya.
            order_reverse True

            ## Nama halaman, yang dapat di edit dengan mengklik tombol.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## Kolom slot file.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("Slot Kosong")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Tombol untuk mengakses halaman lain.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_quicksave:
                        textbutton _("{#quick_page}C") action FilePage("quick")

                    ## antara(1,10) beri nomor antara 1 sampai 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Sinkronisasi Unggah"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Unduh Sinkronisasi"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Layar preferensi/opsi #######################################################
##
## Layar preferensi mengijinkan pemain untuk mengkonfigurasi permainan untuk
## menyesuaikan gaya bermain masing masing individu.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Setting"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Tampilan")
                        textbutton _("Jendela") action Preference("display", "window")
                        textbutton _("Layar Penuh") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "radio"
                    label _("Ukuran Font")
                    textbutton _("Kecil") action Preference("font size", 0.85)
                    textbutton _("Normal") action Preference("font size", 1.0)
                    textbutton _("Besar") action Preference("font size", 1.2)

                vbox:
                    style_prefix "check"
                    label _("Lompati")
                    textbutton _("Belum Terlihat") action Preference("skip", "toggle")
                    textbutton _("Setelah Pilihan") action Preference("after choices", "toggle")
                    textbutton _("Transisi") action InvertSelected(Preference("transitions", "toggle"))

                ## Tipe tambahan vboxes "radio_pref" atau "check_pref" dapat di
                ## tambahkan disini, untuk menambahkan tambahan preferensi yang
                ## dibuat creator.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Kecepatan Text")

                    bar value Preference("text speed")

                    label _("Waktu Otomatis-Maju")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Volume Musik")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Volume Suara")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Tes") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Volume Vokal")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Tes") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Senyapkan Semua"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## Layar Riwayat ###############################################################
##
## Layar yang menampilkan History dialog kepada pemain. Semenjak tidak ada yang
## spesial tentang layar ini, ini memiliki akses ke history dialog yang di
## simpan di _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Hindari mempredisi layar ini, ini dapat berukuran sangat besar.
    predict False

    use game_menu(_("Riwayat"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## Ini menampilkan layar secara semestinya jika history_height
                ## memiliki value None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Mengambil warna dari text 'who' dari karakter, jika
                        ## di set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("Riwayat dialog kosong.")


## Ini menentukan tag apa yang diizinkan ditampilkan di layar sejarah/catatan.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Layar Bantuan ###############################################################
##
## Layar yang memberikan informasi tentang keyboard dan mouse binding. Ini
## menggunakan layar lain (keyboard_help, mouse_help, and gamepad_help) untuk
## menampilkan bantuan yang sebenarnya.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Bantuan"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Papanketik") action SetScreenVariable("device", "keyboard")
                textbutton _("Tetikus") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Masukkan")
        text _("Dialog tingkat lanjut dan mengaktifkan antarmuka.")

    hbox:
        label _("Spasi")
        text _("Dialog tingkat lanjut tanpa memilih pilihan.")

    hbox:
        label _("Tombol Panah")
        text _("Navigasi di antarmuka")

    hbox:
        label _("Melarikan diri")
        text _("Akses menu permainan.")

    hbox:
        label _("Ctrl")
        text _("Lompati dialog ketika di tahan.")

    hbox:
        label _("Tab")
        text _("Nyala/Matikan lompati dialog.")

    hbox:
        label _("Halaman Atas")
        text _("Putar mundur ke dialog sebelumnya.")

    hbox:
        label _("Page Down")
        text _("Putar maju ke dialog berikut.")

    hbox:
        label "H"
        text _("Sembunyikan antarmuka.")

    hbox:
        label "S"
        text _("Ambiil tangkapan layar.")

    hbox:
        label "V"
        text _("Nyalakan assisten {a=https://www.renpy.org/l/voicing}suara-sendiri{/a}")

    hbox:
        label "Shift+A"
        text _("Membuka menu aksesibilitas.")


screen mouse_help():

    hbox:
        label _("Klik Kiri")
        text _("Dialog tingkat lanjut dan mengaktifkan antarmuka.")

    hbox:
        label _("Klik Tengah")
        text _("Sembunyikan antarmuka.")

    hbox:
        label _("Klik Kanan")
        text _("Akses menu permainan.")

    hbox:
        label _("Roda Mouse Atas")
        text _("Putar mundur ke dialog sebelumnya.")

    hbox:
        label _("Roda Mouse Bawah")
        text _("Putar maju ke dialog berikut.")


screen gamepad_help():

    hbox:
        label _("Trigger Kanan\nA/Tombol Bawah")
        text _("Dialog tingkat lanjut dan mengaktifkan antarmuka.")

    hbox:
        label _("Trigger Kiri\nBahu Kiri")
        text _("Putar mundur ke dialog sebelumnya.")

    hbox:
        label _("Pundak Kanan")
        text _("Putar maju ke dialog berikut.")

    hbox:
        label _("D-Pad, Stick")
        text _("Navigasi di antarmuka")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Akses menu permainan.")

    hbox:
        label _("Y/Tombol Atas")
        text _("Sembunyikan antarmuka.")

    textbutton _("Kalibrasi") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Layar Tambahan
################################################################################


## Layar konfirmasi ############################################################
##
## Layar konfirmasi di panggil ketika Ren'Py mau menanyakan ke pemain pertanyaan
## ya atau tidak.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Memastikan layar lain tidak mendapatkan input ketika layar ini di
    ## panggil.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Ya") action yes_action
                textbutton _("Tidak") action no_action

    ## Klik kanan dan jawaban escape "Tidak".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Lompati indikator layar #####################################################
##
## layar skip_indicator di tampilkan untuk mengindikasian proses skipping sedang
## dalam proses.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Melompati")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## transform digunakan untuk mengkedipkan panah setelah yang lain.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## Kami harus menggunakan font yang mempunyai glyph BLACK RIGHT-POINTING
    ## SMALL TRIANGLE didalamnya.
    font "DejaVuSans.ttf"


## Layar pemberitahuan #########################################################
##
## layar notify digunakan untuk menampilkan pesan kepada pemain. (Seperti,
## ketika game di simpan cepat atau screenshot di ambil.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## Layar NVL ###################################################################
##
## Layar ini digunakan untuk dialog dan menu mode-NVL.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Menampilkan dialog pada vpgrid atau vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Menampilkan menu, jika diberikan. Menu dapat ditampilkan dengan tidak
        ## benar jika config.narrator_menu diatur ke True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## Ini mengendalikan angka maksimum entri mode-NVL yang dapat di tampilkan
## sekaligus.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Layar gelembung #############################################################
##
## Layar gelembung digunakan untuk menampilkan dialog kepada pemain saat
## menggunakan gelembung ucapan. Layar gelembung mengambil parameter yang sama
## dengan layar ucapkan, harus membuat tampilan dengan id "apa", dan dapat
## membuat tampilan dengan id "kotak nama", "siapa", dan "jendela".
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

        default ctc = None
        showif ctc:
            add ctc

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Versi Mobile(HP/Handphone/Android)
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Semenjak mouse tidak ada, kami mengganti menu cepat dengan yang menggunakan
## tombol yang lebih besar dan sedikit, yang memudahkan untuk di sentuh.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        textbutton _("☰"):
            style "quick_icon_button"
            xpos 18
            ypos 18
            action ShowMenu("navigation")

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("↩"):
                style "quick_icon_button"
                action Rollback()
            textbutton _("»"):
                style "quick_icon_button"
                action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("A"):
                style "quick_auto_button"
                action Preference("auto-forward", "toggle")


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style game_menu_viewport:
    variant "small"
    xsize 1305

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900


# ========================= HARI 7 =========================

screen day7_unpack_inventory(packed_items):
    modal True
    zorder 120
    default placed = []

    $ labels = {
        "notebook": "Buku catatan",
        "pencil": "Pensil",
        "eraser": "Penghapus",
        "phone": "Ponsel",
        "id_card": "Kartu identitas",
        "water": "Botol minum",
        "earphone": "Earphone",
    }

    add "bg language laboratory"
    add Solid("#02061788")

    frame:
        xalign 0.5
        yalign 0.08
        xsize 1260
        padding (30, 22)
        background Solid("#071923ee")
        vbox:
            spacing 8
            text "HARI UJIAN • SIAPKAN MEJA" xalign 0.5 size 31 bold True color "#67e8f9"
            text "Keluarkan barang yang diperlukan dari tas. Barang lain tetap disimpan agar meja ujian rapi." xalign 0.5 text_align 0.5 size 19 color "#dbeafe"

    frame:
        xalign 0.5
        yalign 0.52
        xsize 920
        ysize 360
        padding (28, 24)
        background Solid("#102b35ee")
        vbox:
            spacing 14
            text "ISI TAS" size 24 bold True color "#fde68a"
            for item_name in packed_items:
                textbutton (("✓  " if item_name in placed else "＋  ") + labels.get(item_name, item_name)):
                    xfill True
                    ysize 52
                    background Solid("#0e7490" if item_name in placed else "#123a42")
                    hover_background Solid("#22d3ee")
                    text_color "#f8fafc"
                    text_size 20
                    action SetScreenVariable("placed", toggle_inventory_item(placed, item_name))

            text "Tidak ada barang wajib. Keluarkan item apa pun yang ingin kamu gunakan saat ujian." size 17 color "#fbbf24"
            textbutton "SELESAI MENATA MEJA  →":
                xalign 1.0
                xsize 340
                ysize 58
                background Solid("#0e7490")
                hover_background Solid("#0891b2")
                insensitive_background Solid("#334155")
                text_color "#ffffff"
                text_insensitive_color "#94a3b8"
                text_size 19
                action Return(placed)


screen day7_unpack_inventory_visual(packed_items):
    modal True
    zorder 120
    default placed = []

    $ labels = {"notebook": "Buku catatan", "pencil": "Pensil", "eraser": "Penghapus", "phone": "Ponsel", "id_card": "Kartu identitas", "water": "Botol minum", "earphone": "Earphone"}
    $ images = {"notebook": "day7 item notebook", "pencil": "day7 item pencil", "eraser": "day7 item eraser", "phone": "day7 item phone", "id_card": "day7 item id_card", "water": "day7 item water", "earphone": "day7 item earphone"}
    $ positions = {"notebook": (650, 610), "pencil": (900, 570), "eraser": (1160, 730), "phone": (1360, 600), "id_card": (460, 700), "water": (540, 550), "earphone": (1120, 570)}

    add "bg day7 exam desk"
    add Solid("#02061755")

    frame:
        xalign 0.5
        yalign 0.08
        xsize 1260
        padding (26, 20)
        background Solid("#071923ee")
        vbox:
            spacing 8
            text "HARI UJIAN  •  SIAPKAN MEJA" xalign 0.5 size 30 bold True color "#67e8f9"
            text "Klik gambar barang di panel tas. Barang yang dipilih akan muncul di atas meja." xalign 0.5 text_align 0.5 size 19 color "#dbeafe"

    for item_name in placed:
        if item_name in positions:
            add Transform(images[item_name], xysize=(150, 150)) xpos positions[item_name][0] ypos positions[item_name][1]

    frame:
        xpos 52
        ypos 330
        xsize 430
        ysize 510
        padding (22, 20)
        background Solid("#071923ee")
        vbox:
            spacing 12
            text "ISI TAS" size 24 bold True color "#fde68a"
            for item_name in packed_items:
                button:
                    xfill True
                    ysize 72
                    padding (8, 5)
                    background Solid("#0e7490" if item_name in placed else "#123a42")
                    hover_background Solid("#22d3ee")
                    action SetScreenVariable("placed", toggle_inventory_item(placed, item_name))
                    add Transform(images.get(item_name, "day7 item notebook"), xysize=(62, 62))
                    text (("✓  " if item_name in placed else "＋  ") + labels.get(item_name, item_name)) xalign 0.72 yalign 0.5 size 18 color "#f8fafc"
            text "Tidak ada barang wajib. Kamu bebas menata item apa pun." size 17 color "#fbbf24" line_spacing 3
            textbutton "SELESAI MENATA MEJA  →":
                xfill True
                ysize 58
                background Solid("#0e7490")
                hover_background Solid("#0891b2")
                text_color "#ffffff"
                text_size 18
                action Return(placed)


screen day7_pre_scan_item_use(placed_items):
    """Interaksi singkat menggunakan barang yang sudah dikeluarkan di meja."""
    modal True
    zorder 124
    default used_items = []
    default hovered_item = None

    $ labels = {"notebook": "Simpan kembali ke tas", "pencil": "Cek pensil", "eraser": "Siapkan penghapus", "phone": "Buka aplikasi ujian", "id_card": "Letakkan kartu identitas", "water": "Buka botol minum", "earphone": "Cek earphone"}
    $ images = {"notebook": "day7 item notebook", "pencil": "day7 item pencil", "eraser": "day7 item eraser", "phone": "day7 item phone", "id_card": "day7 item id_card", "water": "day7 item water", "earphone": "day7 item earphone"}
    $ positions = {"notebook": (650, 610), "pencil": (900, 570), "eraser": (1160, 730), "phone": (1360, 600), "id_card": (460, 700), "water": (540, 550), "earphone": (1120, 570)}

    add "bg day7 exam desk"
    add Solid("#02061766")

    frame:
        xalign 0.5
        yalign 0.08
        xsize 1320
        padding (24, 18)
        background Solid("#071923ee")
        vbox:
            spacing 7
            text "SEBELUM VERIFIKASI  •  GUNAKAN PERLENGKAPAN" xalign 0.5 size 28 bold True color "#67e8f9"
            text "Tekan barang di meja untuk melakukan persiapan singkat. Kamu tidak wajib menggunakan semuanya." xalign 0.5 text_align 0.5 size 18 color "#dbeafe"

    for item_name in placed_items:
        if item_name in positions:
            button:
                xpos positions[item_name][0]
                ypos positions[item_name][1]
                xsize 190
                ysize 190
                padding (0, 0)
                background None
                hover_background None
                hovered SetScreenVariable("hovered_item", item_name)
                unhovered SetScreenVariable("hovered_item", None)
                action SetScreenVariable("used_items", toggle_inventory_item(used_items, item_name))
                if hovered_item == item_name:
                    add Transform(images[item_name], xysize=(185, 185), matrixcolor=BrightnessMatrix(0.35))
                else:
                    add Transform(images[item_name], xysize=(170, 170))
                text ("✓ " if item_name in used_items else "") + labels.get(item_name, item_name):
                    xalign 0.5
                    yalign 1.0
                    text_align 0.5
                    size 15
                    bold True
                    color "#f8fafc"

    frame:
        xpos 48
        ypos 335
        xsize 470
        ysize 520
        padding (22, 20)
        background Solid("#071923ee")
        vbox:
            spacing 10
            text "PERSIAPAN MEJA" size 24 bold True color "#fde68a"
            text "[len(used_items)] / [len(placed_items)] barang digunakan" size 18 color "#cbd5e1"
            for item_name in placed_items:
                text ("✓  " if item_name in used_items else "○  ") + labels.get(item_name, item_name) size 17 color ("#a7f3d0" if item_name in used_items else "#94a3b8")
            null height 8
            if hovered_item:
                text labels.get(hovered_item, hovered_item) size 18 bold True color "#67e8f9"
                text "Klik lagi untuk membatalkan atau mengulang persiapan item." size 15 color "#cbd5e1" line_spacing 2
            else:
                text "Barang yang belum digunakan tetap berada di meja dan akan ikut terlihat saat verifikasi ruangan." size 15 color "#fbbf24" line_spacing 3
            textbutton "LANJUT KE VERIFIKASI  →":
                xfill True
                ysize 60
                background Solid("#0e7490")
                hover_background Solid("#0891b2")
                text_color "#ffffff"
                text_size 19
                action Return(used_items)


screen day7_face_scan():
    modal True
    zorder 125
    default scan_state = "idle"

    add Solid("#020617e8")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 980
        ysize 700
        padding (38, 32)
        background Solid("#071923f5")
        vbox:
            spacing 18
            text "VERIFIKASI PESERTA" xalign 0.5 size 32 bold True color "#67e8f9"
            text "Arahkan wajah ke kamera ponsel untuk memulai ujian simulasi." xalign 0.5 text_align 0.5 size 20 color "#dbeafe"
            frame:
                xalign 0.5
                xsize 430
                ysize 300
                padding (18, 18)
                background Solid("#0f3440")
                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 12
                    text "◉" xalign 0.5 size 100 color ("#4ade80" if scan_state == "done" else "#67e8f9")
                    text ("WAJAH TERDETEKSI" if scan_state == "done" else "KAMERA SIAP") xalign 0.5 size 22 bold True color "#f8fafc"
                    text ("Identitas cocok dengan data pendaftaran." if scan_state == "done" else "Pastikan wajah berada di dalam bingkai.") xalign 0.5 text_align 0.5 size 17 color "#cbd5e1"
            if scan_state == "done":
                textbutton "LANJUT KE SCAN RUANGAN  →":
                    xalign 0.5
                    xsize 400
                    ysize 62
                    background Solid("#0e7490")
                    hover_background Solid("#0891b2")
                    text_color "#ffffff"
                    text_size 20
                    action Return(True)
            else:
                textbutton "MULAI SCAN WAJAH":
                    xalign 0.5
                    xsize 350
                    ysize 62
                    background Solid("#164e63")
                    hover_background Solid("#0e7490")
                    text_color "#cffafe"
                    text_size 20
                    action SetScreenVariable("scan_state", "done")


screen day7_face_scan_englishscore():
    """Simulasi pemeriksaan liveness bergaya aplikasi EnglishScore."""
    modal True
    zorder 126
    default stage = 0
    default checks = []

    add "bg day7 exam classroom"
    add Solid("#020617aa")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1080
        ysize 790
        padding (34, 28)
        background Solid("#050b12f2")
        vbox:
            spacing 14
            text "ENGLISHCORE  •  IDENTITY CHECK" xalign 0.5 size 28 bold True color "#67e8f9"
            text "Pemeriksaan liveness dan identitas peserta" xalign 0.5 size 18 color "#cbd5e1"
            hbox:
                xalign 0.5
                spacing 10
                for step, label in [(0, "1  WAJAH"), (1, "2  LIVENESS"), (2, "3  SELESAI")]:
                    frame:
                        xsize 210
                        ysize 42
                        background Solid("#0e7490" if stage >= step else "#1e293b")
                        text label xalign 0.5 yalign 0.5 size 15 bold True color "#ffffff"
            frame:
                xalign 0.5
                xsize 470
                ysize 385
                padding (18, 18)
                background Solid("#0f3440")
                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 10
                    text "◯" xalign 0.5 size 170 color ("#4ade80" if stage >= 2 else "#67e8f9")
                    text ("IDENTITAS TERVERIFIKASI" if stage >= 2 else ("LIVENESS CHECK AKTIF" if stage == 1 else "POSISIKAN WAJAH DI DALAM LINGKARAN")) xalign 0.5 text_align 0.5 size 20 bold True color "#f8fafc"
                    text ("Wajah cocok dengan data peserta." if stage >= 2 else ("Ikuti instruksi untuk memastikan kamera melihat orang sungguhan." if stage == 1 else "Pastikan pencahayaan cukup dan wajah terlihat jelas.")) xalign 0.5 text_align 0.5 xsize 390 size 16 color "#cbd5e1"
            frame:
                xalign 0.5
                xsize 760
                padding (16, 12)
                background Solid("#0b1f2e")
                vbox:
                    spacing 7
                    text "STATUS PEMERIKSAAN" size 17 bold True color "#fde68a"
                    text ("✓ Kamera siap" if stage >= 0 else "○ Kamera siap") size 16 color "#a7f3d0"
                    text ("✓ Wajah terdeteksi" if stage >= 1 else "○ Wajah terdeteksi") size 16 color ("#a7f3d0" if stage >= 1 else "#94a3b8")
                    text ("✓ Gerakan alami terverifikasi" if stage >= 2 else "○ Gerakan alami terverifikasi") size 16 color ("#a7f3d0" if stage >= 2 else "#94a3b8")
            if stage == 0:
                textbutton "MULAI FACE CHECK":
                    xalign 0.5
                    xsize 390
                    ysize 60
                    background Solid("#0e7490")
                    hover_background Solid("#0891b2")
                    text_color "#ffffff"
                    text_size 19
                    action SetScreenVariable("stage", 1)
            elif stage == 1:
                textbutton "LIHAT KE KAMERA  •  TAHAN 2 DETIK":
                    xalign 0.5
                    xsize 470
                    ysize 60
                    background Solid("#0e7490")
                    hover_background Solid("#0891b2")
                    text_color "#ffffff"
                    text_size 18
                    action SetScreenVariable("stage", 2)
            else:
                textbutton "LANJUT KE SCAN RUANGAN  →":
                    xalign 0.5
                    xsize 440
                    ysize 60
                    background Solid("#16a34a")
                    hover_background Solid("#22c55e")
                    text_color "#ffffff"
                    text_size 18
                    action Return(True)


screen day7_room_scan():
    modal True
    zorder 125
    default scanned = []
    $ scan_labels = {"door": "Pintu keluar", "desk": "Meja ujian", "window": "Jendela", "camera": "Kamera pengawas"}
    $ scan_required = ["door", "desk", "window", "camera"]

    add "bg language laboratory"
    add Solid("#02061788")
    frame:
        xalign 0.5
        yalign 0.08
        xsize 1220
        padding (30, 22)
        background Solid("#071923ee")
        vbox:
            spacing 8
            text "SCAN RUANGAN UJIAN" xalign 0.5 size 31 bold True color "#67e8f9"
            text "Tekan semua titik penting untuk memastikan ruangan aman dan sesuai prosedur." xalign 0.5 text_align 0.5 size 19 color "#dbeafe"

    for item_name, item_pos in [("door", (300, 350)), ("desk", (860, 570)), ("window", (1300, 280)), ("camera", (1530, 150))]:
        textbutton (("✓ " if item_name in scanned else "SCAN ") + scan_labels[item_name]):
            xpos item_pos[0]
            ypos item_pos[1]
            xsize 250
            ysize 60
            background Solid("#0e7490dd" if item_name in scanned else "#0b1f2ecc")
            hover_background Solid("#22d3eeef")
            text_color "#f8fafc"
            text_size 17
            action SetScreenVariable("scanned", toggle_inventory_item(scanned, item_name))

    frame:
        xalign 0.86
        yalign 0.58
        xsize 420
        ysize 245
        padding (24, 20)
        background Solid("#071923ee")
        vbox:
            spacing 10
            text "STATUS SCAN" size 23 bold True color "#fde68a"
            text "[len(scanned)] / 4 titik diperiksa" size 19 color "#cbd5e1"
            text "✓ Semua titik harus terverifikasi sebelum ujian dimulai." size 17 color "#94a3b8" line_spacing 3
            textbutton "KUNCIKAN RUANGAN  →":
                xfill True
                ysize 56
                background Solid("#0e7490" if all(item in scanned for item in scan_required) else "#334155")
                hover_background Solid("#0891b2")
                text_color "#ffffff"
                text_insensitive_color "#94a3b8"
                text_size 18
                sensitive all(item in scanned for item in scan_required)
                action Return(True)


screen day7_room_scan_drag(placed_items=None):
    modal True
    zorder 125
    $ scan_labels = {"door": "PINTU", "desk": "MEJA", "window": "JENDELA", "camera": "KAMERA"}
    $ scan_positions = {"door": (260, 330), "desk": (820, 610), "window": (1340, 300), "camera": (1540, 150)}
    $ item_images = {"notebook": "day7 item notebook", "pencil": "day7 item pencil", "eraser": "day7 item eraser", "phone": "day7 item phone", "id_card": "day7 item id_card", "water": "day7 item water", "earphone": "day7 item earphone"}

    add "bg day7 exam desk"
    add Solid("#02061744")

    # Barang yang tadi dikeluarkan tetap terlihat di meja selama proses scan.
    if placed_items:
        for index, item_name in enumerate(placed_items):
            add Transform(item_images.get(item_name, "day7 item notebook"), xysize=(130, 130)) xpos (720 + (index % 4) * 170) ypos (650 + (index // 4) * 75)

    frame:
        xalign 0.5
        yalign 0.08
        xsize 1220
        padding (24, 18)
        background Solid("#071923ee")
        vbox:
            spacing 7
            text "SCAN RUANGAN  •  GESER PONSEL KE TARGET" xalign 0.5 size 28 bold True color "#67e8f9"
            text "Seret smartphone ke reticle PINTU, MEJA, JENDELA, dan KAMERA. Lepaskan untuk memindai." xalign 0.5 text_align 0.5 size 18 color "#dbeafe"

    draggroup:
        for point_name, point_pos in scan_positions.items():
            drag:
                drag_name ("scan_" + point_name)
                draggable False
                droppable True
                xpos point_pos[0]
                ypos point_pos[1]
                xsize 250
                ysize 110
                frame:
                    xfill True
                    yfill True
                    background Solid("#22d3ee66" if point_name in day_7_scanned_points else "#0b1f2eaa")
                    padding (12, 10)
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        text ("✓ " if point_name in day_7_scanned_points else "◎") xalign 0.5 size 30 color ("#4ade80" if point_name in day_7_scanned_points else "#67e8f9")
                        text scan_labels[point_name] xalign 0.5 size 16 bold True color "#f8fafc"

        drag:
            drag_name "scan_phone"
            draggable True
            droppable False
            dragged day7_phone_dragged
            xpos 80
            ypos 170
            xsize 210
            ysize 390
            frame:
                xfill True
                yfill True
                padding (14, 16)
                background Solid("#050b12ee")
                vbox:
                    spacing 10
                    text "SCAN CAM" xalign 0.5 size 15 bold True color "#67e8f9"
                    frame:
                        xfill True
                        ysize 245
                        background Solid("#082f3b")
                        vbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 7
                            text "⌗" xalign 0.5 size 72 color "#a5f3fc"
                            text "DRAG ME" xalign 0.5 size 14 color "#cffafe"
                    text "[len(day_7_scanned_points)] / 4" xalign 0.5 size 22 bold True color "#fde68a"
                    text "Geser ponsel" xalign 0.5 text_align 0.5 size 14 color "#cbd5e1"

    frame:
        xalign 0.93
        yalign 0.86
        xsize 390
        padding (18, 16)
        background Solid("#071923ee")
        vbox:
            spacing 8
            text "PROSEDUR" size 19 bold True color "#fde68a"
            text "Scan aktif setelah ponsel dilepas pada setiap reticle." size 16 color "#cbd5e1" line_spacing 3
            textbutton "LANJUT KE UJIAN  →":
                xfill True
                ysize 56
                background Solid("#0e7490" if len(day_7_scanned_points) == 4 else "#334155")
                hover_background Solid("#0891b2")
                text_color "#ffffff"
                text_insensitive_color "#94a3b8"
                text_size 18
                sensitive len(day_7_scanned_points) == 4
                action Return(True)


screen day7_room_camera_scan(placed_items=None):
    modal True
    zorder 125
    $ scan_labels = {"door": "PINTU KELUAR", "desk": "MEJA PESERTA", "window": "JENDELA", "camera": "KAMERA PENGAWAS"}
    $ scan_positions = {"door": (210, 360), "desk": (820, 620), "window": (1330, 300), "camera": (1530, 160)}
    $ item_images = {"notebook": "day7 item notebook", "pencil": "day7 item pencil", "eraser": "day7 item eraser", "phone": "day7 item phone", "id_card": "day7 item id_card", "water": "day7 item water", "earphone": "day7 item earphone"}

    # Kamera belakang menyorot meja ujian pemain, bukan mockup handphone.
    add "bg day7 exam desk"
    add Solid("#02061733")
    if placed_items:
        for index, item_name in enumerate(placed_items):
            if item_name != "phone":
                add Transform(item_images.get(item_name, "day7 item notebook"), xysize=(100, 100)) xpos (850 + (index % 4) * 120) ypos (650 + (index // 4) * 65)

    frame:
        xalign 0.5
        yalign 0.06
        xsize 1450
        padding (22, 14)
        background Solid("#050b12bb")
        hbox:
            xfill True
            text "● REC  •  KAMERA BELAKANG" size 21 bold True color "#fb7185"
            text "SCAN LINGKUNGAN UJIAN" xalign 0.5 size 26 bold True color "#f8fafc"
            text "[len(day_7_scanned_points)] / 4" xalign 1.0 size 21 color "#a7f3d0"

    draggroup:
        for point_name, point_pos in scan_positions.items():
            drag:
                drag_name ("scan_" + point_name)
                draggable False
                droppable True
                xpos point_pos[0]
                ypos point_pos[1]
                xsize 260
                ysize 120
                frame:
                    xfill True
                    yfill True
                    background Solid("#22d3ee66" if point_name in day_7_scanned_points else "#02061766")
                    padding (12, 8)
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        text ("✓" if point_name in day_7_scanned_points else "⌖") xalign 0.5 size 34 color ("#4ade80" if point_name in day_7_scanned_points else "#67e8f9")
                        text scan_labels[point_name] xalign 0.5 size 15 bold True color "#ffffff"

        # Reticle kamera, tanpa gambar handphone. Pemain menggeser reticle seperti mengarahkan kamera belakang.
        drag:
            drag_name "camera_reticle"
            draggable True
            droppable False
            dragged day7_phone_dragged
            xpos 870
            ypos 420
            xsize 210
            ysize 210
            frame:
                xfill True
                yfill True
                background Solid("#67e8f922")
                padding (8, 8)
                text "⌗" xalign 0.5 yalign 0.5 size 115 color "#ecfeff"

    frame:
        xalign 0.92
        yalign 0.86
        xsize 430
        padding (18, 16)
        background Solid("#050b12dd")
        vbox:
            spacing 8
            text "KAMERA BELAKANG AKTIF" size 20 bold True color "#67e8f9"
            text "Mode kamera mirip EnglishScore: arahkan reticle ke objek dan lepaskan saat target masuk bingkai." size 16 color "#cbd5e1" line_spacing 3
            add Solid("#1e5363") xsize 394 ysize 2
            text "STATUS TEKNIS" size 16 bold True color "#fde68a"
            text "✓ Izin kamera        AKTIF" size 15 color "#a7f3d0"
            text "✓ Pencahayaan        OK" size 15 color "#a7f3d0"
            text ("✓ Objek terdeteksi    %d / 4" % len(day_7_scanned_points)) size 15 color ("#a7f3d0" if len(day_7_scanned_points) == 4 else "#fbbf24")
            text "Pemeriksaan lingkungan tersimpan. Lanjutkan setelah semua titik terdeteksi." size 14 color "#94a3b8" line_spacing 2
            textbutton "SELESAI SCAN  →":
                xfill True
                ysize 56
                background Solid("#0e7490" if len(day_7_scanned_points) == 4 else "#334155")
                hover_background Solid("#0891b2")
                text_color "#ffffff"
                text_insensitive_color "#94a3b8"
                text_size 18
                sensitive len(day_7_scanned_points) == 4
                action Return(True)


screen day7_exam_question(question_number, total_questions, section_label, prompt, option_a, option_b, option_c, previous_score, hint_text=None):
    modal True
    zorder 130
    add Solid("#020617e8")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1280
        ysize 820
        padding (38, 30)
        background Solid("#071923f7")
        vbox:
            spacing 17
            hbox:
                xfill True
                text "SIMULASI TOEFL • [section_label]" size 24 bold True color "#67e8f9"
                text "SOAL [question_number]/[total_questions]" xalign 1.0 size 20 color "#fde68a"
            text "MODE UJIAN DI PONSEL" xalign 0.5 size 16 bold True color "#94a3b8"
            text prompt xsize 1190 size 29 bold True color "#f8fafc" line_spacing 5 substitute False
            add Solid("#1e5363") xsize 1190 ysize 2
            use study_hint_panel(previous_score, hint_text or study_hint_for("mixed"))
            for option, label in [("a", option_a), ("b", option_b), ("c", option_c)]:
                button:
                    xfill True
                    ysize 82
                    padding (24, 14)
                    background Solid("#123a42")
                    hover_background Solid("#0e7490")
                    action Return(option)
                    text (option.upper() + ".  " + label) xsize 1130 yalign 0.5 size 24 color "#ecfeff" substitute False


screen day7_exam_question_phone(question_number, total_questions, section_label, prompt, option_a, option_b, option_c, previous_score, hint_text=None, audio_file=None, time_limit=45):
    modal True
    zorder 130
    default hint_visible = False
    default replay_count = 0
    default time_left = time_limit

    # Setiap soal memiliki countdown sendiri. Habis waktu langsung pindah tanpa dialog sistem.
    timer 1.0 repeat True action If(time_left <= 1, Return("__timeout__"), SetScreenVariable("time_left", time_left - 1))

    if audio_file:
        on "show" action Play("listening", audio_file, loop=False)
        on "hide" action Stop("listening")
        on "replaced" action Stop("listening")
    $ hint_level = study_hint_level(previous_score)

    add "bg day7 exam desk"
    add Solid("#02061755")

    # Smartphone mockup: soal, pilihan, hint, dan progress berada di dalam aplikasi.
    frame:
        xalign 0.5
        yalign 0.5
        xsize 760
        ysize 960
        padding (18, 18)
        background Solid("#050b12f5")
        vbox:
            spacing 10
            frame:
                xfill True
                ysize 42
                padding (14, 8)
                background Solid("#111827")
                hbox:
                    xfill True
                    text "09:41" size 16 color "#e5e7eb"
                    text "ENGLISHCORE SIMULATION" xalign 0.5 size 15 bold True color "#67e8f9"
                    text "▮▮▮ 100%" xalign 1.0 size 15 color "#a7f3d0"

            frame:
                xfill True
                yfill True
                padding (28, 24)
                background Solid("#f8fafc")
                vbox:
                    spacing 14
                    hbox:
                        xfill True
                        text section_label size 19 bold True color "#0f766e" substitute False
                        text "[question_number]/[total_questions]" xalign 1.0 size 18 color "#475569"
                    hbox:
                        xfill True
                        text "WAKTU TERSISA" size 14 bold True color "#64748b"
                        text "[time_left] dtk" xalign 1.0 size 16 bold True color ("#dc2626" if time_left <= 10 else "#0f766e")
                    bar:
                        value time_left
                        range time_limit
                        xfill True
                        ysize 8
                        left_bar Solid("#ef4444" if time_left <= 10 else "#14b8a6")
                        right_bar Solid("#cbd5e1")
                    bar:
                        value question_number
                        range total_questions
                        xfill True
                        ysize 10
                        left_bar Solid("#14b8a6")
                        right_bar Solid("#cbd5e1")
                    if audio_file:
                        text "● AUDIO LISTENING AKTIF" size 15 bold True color "#be123c"
                        textbutton "PUTAR ULANG AUDIO":
                            xalign 1.0
                            ysize 40
                            background Solid("#ffe4e6")
                            hover_background Solid("#fecdd3")
                            text_color "#9f1239"
                            text_size 14
                            sensitive replay_count < 1
                            action [SetScreenVariable("replay_count", replay_count + 1), Play("listening", audio_file, loop=False)]
                    text prompt:
                        xsize 640
                        size 25
                        bold True
                        color "#0f172a"
                        line_spacing 5
                        substitute False

                    if hint_level > 0:
                        textbutton ("TUTUP MATERI" if hint_visible else "TERJEMAHAN & HINT • LV [hint_level]"):
                            xfill True
                            ysize 48
                            background Solid("#ccfbf1")
                            hover_background Solid("#99f6e4")
                            text_color "#115e59"
                            text_size 16
                            action SetScreenVariable("hint_visible", not hint_visible)
                        if hint_visible:
                            frame:
                                xfill True
                                padding (14, 10)
                                background Solid("#ecfeff")
                                text (hint_text or study_hint_for("mixed")) xsize 610 size 17 color "#164e63" line_spacing 3 substitute False
                    else:
                        text "Hint akan terbuka berdasarkan skor akumulasi hari sebelumnya." xsize 620 size 15 color "#64748b"

                    null height 2
                    for option, label in [("a", option_a), ("b", option_b), ("c", option_c)]:
                        textbutton (option.upper() + ".  " + label):
                            xfill True
                            ysize 76
                            padding (16, 12)
                            background Solid("#e2e8f0")
                            hover_background Solid("#99f6e4")
                            text_color "#0f172a"
                            text_size 19
                            action Return(option)

                    text "Jawab satu pilihan untuk melanjutkan. Semua soal akan diselesaikan sebelum hasil akhir." xalign 0.5 text_align 0.5 xsize 620 size 15 color "#64748b" line_spacing 3


screen day7_final_result(total_score, exam_score, passed, ending_title="ENDING", cheating=False, cheating_items=None):
    modal True
    zorder 140
    add Solid("#020617e8")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        padding (44, 38)
        background Solid("#071923f7")
        vbox:
            spacing 18
            text "HASIL SIMULASI HARI 7" xalign 0.5 size 34 bold True color "#67e8f9"
            text ending_title xalign 0.5 text_align 0.5 size 23 bold True color "#fbbf24" substitute False
            text ("LULUS TARGET 400" if passed else ("NILAI TIDAK SAH" if cheating else "TARGET BELUM TERCAPAI")) xalign 0.5 size 28 bold True color ("#4ade80" if passed else "#fb7185")
            text "Skor akumulasi: [total_score] / 950" xalign 0.5 size 23 color "#f8fafc"
            text "Skor ujian Hari 7: [exam_score] / 600" xalign 0.5 size 21 color "#fde68a"
            if cheating:
                text "Pemeriksaan pasca-ujian menemukan: [', '.join(cheating_items or [])]. Skor tidak dapat dinyatakan lulus." xalign 0.5 text_align 0.5 xsize 940 size 20 color "#fb7185" line_spacing 5
            else:
                text ("Semua prosedur verifikasi selesai. Hasil simulasi siap dikirim ke Leo." if passed else "Gunakan review dan hint Hari 7 untuk memperbaiki bagian yang masih lemah.") xalign 0.5 text_align 0.5 xsize 940 size 20 color "#cbd5e1" line_spacing 5
            textbutton "LANJUTKAN":
                xalign 0.5
                xsize 300
                ysize 62
                background Solid("#0e7490")
                hover_background Solid("#0891b2")
                text_color "#ffffff"
                text_size 21
                action Return(True)


screen day7_review_panel(total_score, exam_score, ending_title, cheating=False, cheating_items=None):
    modal True
    zorder 150
    add Solid("#020617e8")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1260
        ysize 820
        padding (40, 32)
        background Solid("#071923f7")
        vbox:
            spacing 14
            text "PANEL REVIEW SETELAH ENDING" xalign 0.5 size 30 bold True color "#67e8f9"
            text ending_title xalign 0.5 size 23 bold True color "#fbbf24" substitute False
            text "Hasil dibaca bersama Study Group" xalign 0.5 size 18 color "#cbd5e1"
            add Solid("#1e5363") xsize 1180 ysize 2
            hbox:
                spacing 24
                frame:
                    xsize 560
                    ysize 470
                    padding (24, 20)
                    background Solid("#102b35")
                    vbox:
                        spacing 11
                        text "RINGKASAN SKOR" size 22 bold True color "#fde68a"
                        text "Vocabulary Hari 1: [day_1_vocab_score] / 50" size 18 color "#ecfeff"
                        text "Structure Hari 2: [day_2_structure_score] / 50" size 18 color "#ecfeff"
                        text "Reading Hari 3: [day_3_reading_score] / 50" size 18 color "#ecfeff"
                        text "Listening Hari 4: [day_4_listening_score] / 50" size 18 color "#ecfeff"
                        text "Structure Hari 5: [day_5_structure_score] / 50" size 18 color "#ecfeff"
                        text "Review Hari 6: [day_6_review_score] / 50" size 18 color "#ecfeff"
                        text "Bonus latihan: [extra_practice_score]" size 18 color "#a7f3d0"
                        text "Ujian Hari 7: [exam_score] / 600" size 19 bold True color "#67e8f9"
                        text "TOTAL: [total_score] / 950" size 23 bold True color "#f8fafc"
                        if cheating:
                            text "STATUS: TIDAK SAH" size 20 bold True color "#fb7185"
                            text "Temuan kamera: [', '.join(cheating_items or [])]" size 16 color "#fecaca"
                frame:
                    xsize 560
                    ysize 470
                    padding (24, 20)
                    background Solid("#102b35")
                    vbox:
                        spacing 13
                        text "CATATAN STUDY GROUP" size 22 bold True color "#fde68a"
                        text "Rina: bagian Listening-mu paling stabil setelah latihan keyword." size 18 color "#a7f3d0" line_spacing 4
                        text "Bima: Structure-mu naik karena kamu berhenti menebak dari satu kata." size 18 color "#93c5fd" line_spacing 4
                        text "Maya: Reading-mu kuat ketika kamu menunjuk bukti langsung di passage." size 18 color "#f9a8d4" line_spacing 4
                        text "Leo: pertahankan strategi dan gunakan log kesalahan untuk simulasi berikutnya." size 18 color "#c4b5fd" line_spacing 4
                        text "Review ini dapat dibuka kembali dari menu hasil Hari 7." size 17 color "#94a3b8" line_spacing 4
            hbox:
                xalign 0.5
                spacing 16
                textbutton "REVIEW HARI 7":
                    xsize 220
                    ysize 58
                    background Solid("#164e63")
                    hover_background Solid("#0891b2")
                    text_color "#ffffff"
                    text_size 19
                    action Return("review")
                textbutton "GANTI HARI":
                    xsize 220
                    ysize 58
                    background Solid("#164e63")
                    hover_background Solid("#0891b2")
                    text_color "#ffffff"
                    text_size 19
                    action Return("switch")
                textbutton "TUTUP PANEL REVIEW":
                    xsize 320
                    ysize 58
                    background Solid("#0e7490")
                    hover_background Solid("#0891b2")
                    text_color "#ffffff"
                    text_size 19
                    action Return("next")
