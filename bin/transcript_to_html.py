#!/usr/bin/env python3

import subprocess
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

sec_headers: dict[str, tuple[str, int]] = {
    "[h3]": ("h3", 2),
    "[h2]": ("h2", 1),
    "[h1]": ("h1", 0),
    "[section]": ("h2", 1),
}
sec_header_keys = list(sec_headers.keys())
generate_sections = True
# "[suppress_sections]"

print(f"have {len(sys.argv)} args")
if len(sys.argv) < 3:
    print(f"usage: {sys.argv[0]} <text> <media> [out=<output>] [<title> [<space_url> [<sec_offset>] ]]")
    print("text file might contain:")
    print("a) '#' at line start to ignore rest of line")
    print("b) '[suppress_sections]' to deactivate sections and TOC output")
    print("c) section headers by starting line with one of:", end="")
    for hdr in sec_header_keys:
        print(f" {hdr}", end="")
    print()
    print("d) Speaker names/replacements, defined starting with '[SPEAKER_NN]'")
    print("  accounts can be put there separed by spaces starting with 'https://' ..")
    sys.exit(0)

narg = 1
text_file = sys.argv[narg]
narg = narg + 1

media_file = sys.argv[narg]
narg = narg + 1

out_file = str( Path(text_file).with_suffix(".html") )
if narg < len(sys.argv) and sys.argv[narg].startswith("out="):
    out_file = sys.argv[narg][4:]
    narg = narg + 1
if out_file == text_file:
    out_file = str( Path(text_file).with_suffix(".html") )

title = sys.argv[narg] if narg < len(sys.argv) else text_file
narg = narg + 1

space_url = sys.argv[narg] if narg < len(sys.argv) else ""
narg = narg + 1

sec_offset = int(sys.argv[narg]) if narg < len(sys.argv) else 0
narg = narg + 1

print(f"{text_file=}")
print(f"{media_file=}")
print(f"{out_file=}")
print(f"{title=}")

if media_file.endswith(".aac"):
    print()
    mp4 = media_file[:-4] + ".mp4"
    if Path(mp4).exists():
        print(f"warning: replacing/using media by {mp4}")
    else:
        print(f"converting media to .mp4 '{mp4}' - necessary for quick jumps.")
        print(f"ffmpeg -i {media_file} -c:v copy -c:a aac {mp4}")
        subprocess.run(['ffmpeg', '-i', media_file, "-c:v", "copy", "-c:a", "aac", mp4])
    media_file = mp4

print()

script_from_text = text_file
if script_from_text.endswith(".txt"):
    script_from_text = script_from_text[0:-4]
script_from_text = script_from_text + "-to-html.sh"
# print(f"{script_from_text=}")
call_args = deepcopy(sys.argv)
for idx, arg in enumerate(call_args):
    if " " in arg or "\t" in arg:
        call_args[idx] = '"' + arg + '"'
with open(script_from_text, "w", encoding="utf-8") as scriptf:
    print(" ".join(call_args), file=scriptf)


@dataclass
class _Section:
    no: int     # for label
    hno: tuple[str, int]  # ref to sec_headers: html header tag, indent
    html_desc: str       # html desc
    prev_t: str
    next_t: str


def get_speaker_name(speaker: str, speakers: dict[str, str]) -> str:
    name_of_speaker = speakers.get(speaker, "")
    if len(name_of_speaker) <= 0:
        name_of_speaker = speaker
    return name_of_speaker


def is_speaker_to_print(speaker: str, speakers: dict[str, str], accounts: dict[str, str]) -> bool:
    name_of_speaker = get_speaker_name(speaker, speakers)
    account_of_speaker = accounts.get(speaker, "")
    for other_speaker, other_name in speakers.items():
        other_account = accounts.get(other_speaker, "")
        other_name = get_speaker_name(other_speaker, speakers)
        if name_of_speaker == other_name and len(account_of_speaker) < len(other_account):
            return False
    return True


with open(out_file, "w") as outf:
    print("<!doctype html>", file=outf)
    print("<html lang=de>", file=outf)
    print("<head>", file=outf)
    print("<meta charset=utf-8>", file=outf)
    print(f"<title>{title}</title>", file=outf)
    print("</head>", file=outf)
    print("<body>", file=outf)

    if space_url:
        print(f"<p>Transkript von <a href=\"{space_url}\" target=\"_blank\">{space_url}</a></p>", file=outf)
        print("<br>", file=outf)

    print("<p>Links sind die anklickbaren Sprungmarken in Sekunden, die direkt zu dieser Stelle im Audio springen.</p>", file=outf)
    # print("<br>", file=outf)
    print("<p>Nutzen sie den Browser 'Auf Seite suchen' .. um Stichworte zu suchen (üblicherweise mit 'Strg-F').</p>", file=outf)
    print("<p>Beachte: das Transkript kann Fehler enthalten! Schreibfehler, falsche Sprecherzuordnungen bis hin zu fehlendem oder falschem Text!</p>", file=outf)
    print("<br>", file=outf)

    outLn: list[str] = []
    sections: list[_Section] = []
    speakers: dict[str, str] = {}  # key: "SPEAKER_NN", value: "name" to replace with
    accounts: dict[str, str] = {}  # key: "SPEAKER_NN", value: "https://..."
    section_no = 0
    prev_line_t = ""
    last_section: _Section | None = None

    with open(text_file, "r") as tf:
        for lno, line in enumerate(tf):

            if line.startswith("#"):
                continue
            if line.startswith("[suppress_sections]"):
                generate_sections = False
                continue
            is_section = False
            for sec_hdr in sec_header_keys:
                if line.startswith(sec_hdr):
                    if generate_sections:
                        hdr = line[len(sec_hdr):].strip()
                        hdr_as_html = hdr.replace("<", "&lt;").replace(">", "&gt;")
                        hno = sec_headers[sec_hdr]
                        section_no = section_no + 1
                        sections.append(_Section(no=section_no, hno=hno, html_desc=hdr_as_html, prev_t=prev_line_t, next_t=""))
                        last_section = sections[-1]
                        outLn.append(f"<a name=\"Label{section_no}\">")
                        outLn.append(f"<{hno[0]}>{hdr_as_html}</{hno[0]}>")
                    is_section = True
                    break
            if line.startswith("[SPEAKER_"):
                is_section = True
                end_pos = line.find("]")
                if end_pos < 1:
                    print(f"warning: no ']' in line {lno + 1}. ignoring: {line.strip()}")
                elif end_pos > 2:
                    speaker = line[1:end_pos]
                    name = line[end_pos + 1:].strip()
                    end_pos = name.find("https://")
                    if end_pos > 0:
                        account = name[end_pos:].strip()
                        name = name[0:end_pos].strip()
                        accounts[speaker] = account
                    speakers[speaker] = name
            if is_section:
                continue

            end_pos = line.find("]")
            if end_pos < 1:
                print(f"warning: no ']' in line {lno+1}. ignoring: {line.strip()}")
                continue
            content = line[end_pos+1:].strip()
            start_pos = line.find("[")
            if start_pos < 0:
                print(f"warning: no '[' in line {lno+1}. ignoring: {line.strip()}")
                continue
            dec_pos = line[start_pos+1:].find(".")
            if start_pos < 0:
                print(f"warning: no '.' in line {lno+1}. ignoring: {line.strip()}")
                continue
            offset = line[start_pos+1:start_pos+1+dec_pos]
            # lf_pos = content.find("\n")
            # print(f"{offset}  {lf_pos}  {content}")
            # print(f"{offset}  {content}")
            for speaker, name in speakers.items():
                content = content.replace(f"{speaker} :", f"{name}:")
                content = content.replace(speaker, name)
            cont_code = content.replace("<", "&lt;").replace(">", "&gt;")
            # print(f"<a href=\"{media_file}#t={offset}\" target=\"_blank\">{offset}</a>", end="", file=outf)
            off_off = str(int(offset) - sec_offset)
            Ln = f"<a href=\"{media_file}#t={off_off}\" target=\"_blank\">{off_off}</a>"
            try:
                sec = int(offset)
                hour = sec // (60 * 60)
                sec = sec - hour * 60 * 60
                min = sec // 60
                sec = sec - min * 60
            except:
                pass
            else:
                if (hour):
                    tstr = f" {hour:02d}:{min:02d}:{sec:02d}"
                else:
                    tstr = f" {min:02d}:{sec:02d}"
                # print(f" <b><code>{tstr}</code></b>", file=outf)
                prev_line_t = tstr
                if last_section and not last_section.next_t:
                    last_section.next_t = prev_line_t

                Ln = Ln + f" <b>{tstr}</b>"

            # print(f"<a href=\"{media_file}#t={offset}\" target=\"_blank\" title=\"{media_file}#t={offset}\">{offset}</a>", end="", file=outf)
            # print(f"<a mimetype=\"audio/mp4\" href=\"{media_file}#t={offset}\" target=\"_blank\" title=\"{media_file}#t={offset}\">{offset}</a>", end="", file=outf)
            # print(f"<audio src=\"{media_file}#t={offset}\" type=\"audio/mp4\">{media_file}#t={offset}</audio>", file=outf)
            # print(f"<pre>{content}</pre>", file=outf)
            # print(f" <code>{cont_code}</code><br>", file=outf)
            Ln = Ln + f" <code>{cont_code}</code><br>"
            # print(f" <code>{cont_code}</code><br>", file=outf)
            outLn.append(Ln)

    n_speaker = 0
    n_accounts = 0
    for speaker, name in speakers.items():
        account = accounts.get(speaker, "")
        if len(name):
            n_speaker = n_speaker + 1
        if len(account):
            n_accounts = n_accounts + 1

    if n_speaker > 0 or n_accounts > 0:
        print("<a name=\"Label_Speakers\">", file=outf)
        # print("<h2>Speakers / Sprecher</h2>", file=outf)
        print("<h2>Sprecher</h2>", file=outf)
        for speaker, name in speakers.items():
            account = accounts.get(speaker, "")
            speaker_name = get_speaker_name(speaker, speakers)
            if len(account) > 0:
                print(f"<a href=\"{account}\">{speaker_name}</a><br>", file=outf)
            else:
                if is_speaker_to_print(speaker, speakers, accounts):
                    print(f"{name}<br>", file=outf)
                else:
                    print(f"WARNING SPEAKER with name '{speaker_name}' is defined multiple times")

    if generate_sections and len(sections):
        # print("<h2>Table of Contents / Inhalte - Sprungmarken</h2>", file=outf)
        print("<h2>Inhalte - Sprungmarken</h2>", file=outf)
        for section in sections:
            # outLn.append(f"<a name=\"Label{section_no}\">")
            hno = section.hno
            print(f"{section.no}, {hno}, {section.html_desc}")
            for k in range(8 * hno[1]):
                print("&nbsp;", end="", file=outf)
            time_ref = section.next_t if section.next_t else section.prev_t
            time_txt = f" ({time_ref.strip()})" if time_ref else ""
            print(f"<a href=\"#Label{section.no}\">{section.html_desc}{time_txt}</a><br>", file=outf)
        print("<br>")
        print("<br>")

    for line in outLn:
        print(line, file=outf)

    for speaker, name in speakers.items():
        account = accounts.get(speaker, "")
        print(f"replace '{speaker}' by '{name}'\t{account}")

    print("</body>", file=outf)
    print("</html>", file=outf)

print()
print(f"you can use ' . {script_from_text} ' for repeated execution.")
