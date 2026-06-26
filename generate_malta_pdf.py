#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT_PATH = "/home/user/dejan/DL_Project56_Malta_Travel_Product_Internal_Review.pdf"

# ─── Colors ──────────────────────────────────────────────────────────────────
DARK_NAVY   = colors.HexColor("#1A2340")
MID_BLUE    = colors.HexColor("#2E4A7A")
LIGHT_BLUE  = colors.HexColor("#E8EDF5")
ORANGE      = colors.HexColor("#C8521A")
LIGHT_GREY  = colors.HexColor("#F4F4F4")
MED_GREY    = colors.HexColor("#CCCCCC")
RED_WARN    = colors.HexColor("#C0392B")
GREEN_OK    = colors.HexColor("#1E7B4B")
WHITE       = colors.white
BLACK       = colors.black

# ─── Styles ──────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle = S("sTitle",
    fontSize=22, leading=28, textColor=WHITE,
    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)

sSubTitle = S("sSubTitle",
    fontSize=11, leading=14, textColor=colors.HexColor("#BDC8E0"),
    fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)

sH1 = S("sH1",
    fontSize=15, leading=20, textColor=WHITE,
    fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=4)

sH2 = S("sH2",
    fontSize=12, leading=16, textColor=DARK_NAVY,
    fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4)

sH3 = S("sH3",
    fontSize=10, leading=13, textColor=MID_BLUE,
    fontName="Helvetica-Bold", spaceBefore=5, spaceAfter=3)

sBody = S("sBody",
    fontSize=9, leading=13, textColor=BLACK,
    fontName="Helvetica", spaceBefore=2, spaceAfter=2)

sBodySmall = S("sBodySmall",
    fontSize=8, leading=11, textColor=colors.HexColor("#333333"),
    fontName="Helvetica", spaceBefore=1, spaceAfter=1)

sWarn = S("sWarn",
    fontSize=9, leading=12, textColor=RED_WARN,
    fontName="Helvetica-Bold", spaceBefore=2, spaceAfter=2)

sNote = S("sNote",
    fontSize=8, leading=11, textColor=colors.HexColor("#555555"),
    fontName="Helvetica-Oblique", spaceBefore=1, spaceAfter=1)

sBullet = S("sBullet",
    fontSize=9, leading=12, textColor=BLACK,
    fontName="Helvetica", leftIndent=12, spaceBefore=1, spaceAfter=1,
    bulletIndent=4)

sTOC = S("sTOC",
    fontSize=9, leading=13, textColor=MID_BLUE,
    fontName="Helvetica", spaceBefore=1, spaceAfter=1)

sApproval = S("sApproval",
    fontSize=10, leading=14, textColor=DARK_NAVY,
    fontName="Helvetica", spaceBefore=3, spaceAfter=3)

# ─── Helper builders ─────────────────────────────────────────────────────────

def section_header(num, text):
    """Dark navy bar with white section number + title."""
    data = [[Paragraph(f"{num}.  {text}", sH1)]]
    t = Table(data, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t

def subsection_bar(text):
    data = [[Paragraph(text, sH2)]]
    t = Table(data, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("LINEBELOW", (0,0), (-1,-1), 1, MID_BLUE),
    ]))
    return t

def warn_box(text):
    data = [[Paragraph(text, sWarn)]]
    t = Table(data, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FEF0ED")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("BOX", (0,0), (-1,-1), 1, RED_WARN),
    ]))
    return t

def info_box(text):
    data = [[Paragraph(text, sBody)]]
    t = Table(data, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#EBF5EB")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("BOX", (0,0), (-1,-1), 1, GREEN_OK),
    ]))
    return t

def build_table(headers, rows, col_widths=None, stripe=True):
    """Generic table with header row."""
    data = [[Paragraph(h, S("th", fontSize=8, fontName="Helvetica-Bold",
                            textColor=WHITE, leading=11))
             for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), sBodySmall) for c in row])
    if col_widths is None:
        w = 17.5 * cm / len(headers)
        col_widths = [w] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0,0), (-1,0), MID_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("GRID", (0,0), (-1,-1), 0.4, MED_GREY),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GREY] if stripe else [WHITE]),
    ]
    t.setStyle(TableStyle(style))
    return t

def bullets(items):
    out = []
    for item in items:
        out.append(Paragraph(f"<bullet>&bull;</bullet> {item}", sBullet))
    return out

def sp(n=1):
    return Spacer(1, n * 0.25 * cm)

# ─── Cover page ──────────────────────────────────────────────────────────────

def cover_page():
    elems = []
    elems.append(Spacer(1, 3*cm))
    cover_data = [[
        Paragraph("D&amp;L Project56", sSubTitle),
        Paragraph(" "),
    ]]
    # Big title block
    title_block = Table([
        [Paragraph("MALTA TRAVEL PRODUCT POOL", sTitle)],
        [Paragraph("Internal Review Version for Lejla", sSubTitle)],
        [Paragraph("Datum: 26. juni 2026.  |  Verzija: 1.0  |  Status: DRAFT — AWAITING APPROVAL", sSubTitle)],
    ], colWidths=[17.5*cm])
    title_block.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 18),
        ("RIGHTPADDING",  (0,0), (-1,-1), 18),
    ]))
    elems.append(title_block)
    elems.append(sp(3))

    meta = [
        ["Dokument", "DL_Project56_Malta_Travel_Product_Internal_Review.pdf"],
        ["Priprema", "D&L Project56 — AI Research Engine"],
        ["Namena", "Interni approval pregled — ne za distribuciju klijentima"],
        ["Izvor materijala", "3 research bloka spojena bez dupliranja"],
        ["Jezik", "Srpski / balkanski, direktan stil"],
    ]
    mt = Table(meta, colWidths=[5*cm, 12.5*cm])
    mt.setStyle(TableStyle([
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("LEADING",  (0,0), (-1,-1), 13),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("GRID", (0,0), (-1,-1), 0.3, MED_GREY),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, LIGHT_GREY]),
    ]))
    elems.append(mt)
    elems.append(sp(3))
    elems.append(warn_box(
        "INTERNO — nije za klijente. Sadrzi konkretan research, operativne upute i "
        "preporuke za product development. Lejla treba da procita, obelezi stavke i "
        "vrati feedback pre pokretanja produkcije bilo kojeg PDF proizvoda."
    ))
    elems.append(PageBreak())
    return elems

# ─── TOC placeholder ─────────────────────────────────────────────────────────

def toc_page():
    elems = []
    elems.append(section_header("", "Sadrzaj"))
    elems.append(sp(1))
    toc_items = [
        ("1.", "Executive Summary"),
        ("2.", "Malta Positioning — sta prodavati i kako"),
        ("3.", "Best Areas to Stay — tabele po zoni"),
        ("4.", "Beaches — tabela svih plaza"),
        ("5.", "Hidden Gems — top 12"),
        ("6.", "Romantic Spots — top 10"),
        ("7.", "Sunset Spots — top 8"),
        ("8.", "Lokalna hrana"),
        ("9.", "Sta izbegavati — top 15 warninga"),
        ("10.", "3-Day Itinerary"),
        ("11.", "5-Day Itinerary"),
        ("12.", "7-Day Itinerary"),
        ("13.", "Hotel Booking Logic"),
        ("14.", "Manual Hotel QA Checklist"),
        ("15.", "Product Ideas za D&L Project56"),
        ("16.", "LEJLA — Review & Approval"),
    ]
    for num, title in toc_items:
        row_data = [[Paragraph(num, S("tn", fontSize=9, fontName="Helvetica-Bold",
                                      textColor=MID_BLUE, leading=13)),
                     Paragraph(title, sTOC)]]
        rt = Table(row_data, colWidths=[1.2*cm, 16.3*cm])
        rt.setStyle(TableStyle([
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LINEBELOW", (0,0), (-1,-1), 0.3, MED_GREY),
        ]))
        elems.append(rt)
    elems.append(PageBreak())
    return elems

# ─── Section 1: Executive Summary ────────────────────────────────────────────

def section1():
    e = []
    e.append(section_header("1", "Executive Summary"))
    e.append(sp(1))

    e.append(subsection_bar("Zasto Malta ima smisla kao travel product"))
    e += bullets([
        "Kompaktna destinacija: celo ostrvo prelazis za manje od 1h — lako za planiranje 3–7 dana.",
        "Vise od 300 suneanih dana godisnje; more toplo od juna do oktobra.",
        "UNESCO trojka: Valletta, Megalitski hramovi, Hal Saflieni Hypogeum.",
        "Kombinacija istorije + mora + island hoppinga = visoka percipirana vrednost za paket.",
        "Dobro razvijen ferry sistem (Sliema–Valletta, Valletta–Three Cities, Malta–Gozo).",
        "Turisticki segment dominantno mid-range + parovi + porodice = direktno ciljna publika D&L.",
        "Visok USP sunset spotova, romanticnih lokacija i hidden gems — jako prodajno.",
    ])
    e.append(sp(1))

    e.append(subsection_bar("Za koga je dobra"))
    e += bullets([
        "Parovi (sunset + vecere + male distance, romanticni stari gradovi).",
        "First-time travelers (bez logistickog stresa, sve blizu, engleski svugde).",
        "Kratki odmori 3–5 dana.",
        "City-break + beach kombinacija.",
        "Porodice sa starijom decom (planavnske aktivnosti + plaże).",
        "Ljubitelji istorije, fotografije, gastronomije.",
    ])
    e.append(sp(1))

    e.append(subsection_bar("Za koga NIJE dobra"))
    e += bullets([
        "Turisti koji ocekuju ogromne pescane plaze kao Grcka/Turska — vise od 50% obale je kamenita.",
        "All-inclusive resort vibe — ne postoji u tom formatu.",
        "Porodice sa bebama u kolicima (strme ulice, kamene stepenice u Valletti/Mdini).",
        "Klijenti koji ne podnose guzvu u julu/avgustu.",
        "Oni koji traze potpunu tisinu i izolaciju.",
        "Klijenti sa smanjenom pokretljivoscu (topografija je zahtevna).",
    ])
    e.append(sp(1))

    e.append(subsection_bar("Najbolji meseci"))
    months = [
        ["Mesec", "Ocena", "Napomena"],
        ["Maj (kraj) / Juni", "ODLICNO", "Balans temperature, manje guzve, nilje cene"],
        ["Juli / Avgust", "DOBRO za more — TESKO inace", "38–40°C + vlaga, najvece guzve, skuplje"],
        ["Septembar / Oktobar (poc.)", "ODLICNO", "More jos toplo, guzve manje, prijatnija temperatura"],
        ["April / rani Maj", "DOBRO", "Hladnije, kulturne ture, ne za plazu"],
        ["Novembar – Mart", "NIJE za plazu", "Tura destinacija, ne letovalisni segment"],
    ]
    e.append(build_table(months[0], months[1:],
                         col_widths=[4.5*cm, 4.5*cm, 8.5*cm]))
    e.append(sp(1))

    e.append(subsection_bar("Glavni rizici"))
    risks = [
        ("Guzva u avgustu", "Blue Lagoon, Golden Bay, bus linije — katastrofalno pretrpano"),
        ("Prevoz bez auta", "Bus je spor i leti pretrpan; hidden beaches bez auta su problem"),
        ("Pogresna zona smeštaja", "300m do mora moze znaciti stene, ne pesak"),
        ("Blue Lagoon bez bookinga", "Od 2025/2026: QR/booking sistem za pristup obali — mora se planirati"),
        ("Premalo peska", "Vise od 50% obale je kamenita; klijenti moraju znati pre bookinga"),
        ("Construction noise", "Malta je gradiliste; hotel bez provere poslednjih 30-90 recenzija = rizik"),
    ]
    e.append(build_table(["Rizik", "Objasnjenje"], risks,
                         col_widths=[5*cm, 12.5*cm]))
    e.append(PageBreak())
    return e

# ─── Section 2: Positioning ──────────────────────────────────────────────────

def section2():
    e = []
    e.append(section_header("2", "Malta Positioning — sta prodavati i kako"))
    e.append(sp(1))

    e.append(warn_box("NE prodavati Maltu kao 'pure beach resort'. Klijenti ce biti razocaran. "
                      "Prodavati kao: sea + history + island hopping + romantic spots + food + sunsets."))
    e.append(sp(1))

    e.append(subsection_bar("Idealni PDF proizvodi"))
    products = [
        ["Naziv", "Target", "Pain point koji rjesava"],
        ["Malta 3-Day Quick Plan", "First-timers, kratki odmor", "Ne znaju odakle krenuti, boje se da nece stici nista"],
        ["Malta 5-Day Perfect Plan", "Parovi, porodice", "Zele balans plaze + kultura + Gozo, ali ne znaju logistiku"],
        ["Malta 7-Day Full Plan", "Duzi odmor, second-time", "Gozo + Comino + jug Malte + flexible beach dan"],
        ["Romantic Malta PDF", "Parovi, godisnjice", "Gde su pravi romanticni spotovi, zalasci, vecere"],
        ["Family Beach Malta PDF", "Porodice sa decom", "Koje su prave pescane plaze, sta je bezbedno za decu"],
        ["Where to Stay in Malta Guide", "Svi segmenti", "Koja zona je dobra za kog gosta — bez skupih gresaka"],
        ["Malta No-Car Itinerary", "Turisti bez auta", "Sta moze bez rent-a-cara, koje plaze su dostupne busom"],
        ["Malta Hotel Area Mistakes Guide", "Pre-booking faza", "Kako ne knjiziti hotel u pogresnoj zoni"],
        ["Malta Gozo + Comino Plan", "Island hopping fokus", "Logistika trajekta, timing Blue Lagoon, Gozo highlights"],
    ]
    e.append(build_table(products[0], products[1:],
                         col_widths=[5*cm, 4.5*cm, 8*cm]))
    e.append(PageBreak())
    return e

# ─── Section 3: Areas to Stay ────────────────────────────────────────────────

def section3():
    e = []
    e.append(section_header("3", "Best Areas to Stay"))
    e.append(sp(1))
    e.append(Paragraph(
        "Napomena: 'seafront hotel' ne znaci 'beachfront hotel'. Mnogi hoteli uz more imaju kamenitu obalu "
        "ili betonsku promenadu. Uvek proveriti Google Maps satelit pre preporuke.",
        sNote))
    e.append(sp(1))

    headers = ["Area", "Best for", "Avoid if", "Pros", "Cons", "Bez auta?", "Conf."]
    rows = [
        ["Valletta",
         "First-timers, parovi, 3 dana, culture",
         "Zelis plazu ili nightlife",
         "Walkable, UNESCO, restorani, ferry, logistika",
         "Nema plaze, skuplje, tiho nocu",
         "Da — idealna",
         "High"],
        ["Sliema / Gzira",
         "Parovi, porodice starija deca, mid-range",
         "Trazis pescanu plazu ispred hotela",
         "Promenada, restorani, ferry, shopping, prevoz",
         "Nema pescane plaze (rock coast), buka saobracaja",
         "Da — najprakticnija",
         "High"],
        ["St Julian's / Spinola",
         "Mladi parovi, nightlife, restorani",
         "Porodice, light sleepers blizu Paceville",
         "Marina, restorani, waterfront setnja",
         "Paceville buka nocu, guzva",
         "Da",
         "High"],
        ["Paceville",
         "Party travellers",
         "Parovi, porodice, seniors, miran odmor",
         "Klubovi, barovi",
         "Buka do zore, guzva, manje bezbedno noci",
         "Da",
         "High"],
        ["Mellieha",
         "Porodice, beach-first odmor",
         "Zelis Vallettu svaki dan bez auta",
         "Najveca pescana plaza, Gozo ferry blizu",
         "Daleko od centru, bus leti pretrpan",
         "Moze, ali treba strpljenje",
         "High"],
        ["St Paul's Bay / Bugibba / Qawra",
         "Budget / porodice / seniors",
         "Trazis sarm, romantiku, stari grad",
         "Jeftiniji smestaj, boat trips, akvarijum",
         "Estetski neprivlacno, turisticka masa",
         "Da",
         "Medium"],
        ["Three Cities / Birgu",
         "Parovi, slow travel, fotografija",
         "Zelis nightlife i mnogo hotela",
         "Autentican ambijent, harbour views, ferry Valletta",
         "Malo hotela, nema plaze",
         "Da (ferry)",
         "High"],
        ["Mdina / Rabat",
         "Parovi, luxury, godisnjice",
         "Zelis centralnu bazu svaki dan bez auta",
         "Najromanticniji old-town, poseban osecaj uvece",
         "Slabija logistika za plaze, manje smestaja",
         "Ne — preporucuje se auto",
         "Medium"],
        ["Gozo (Victoria/Xlendi/Marsalforn)",
         "Parovi, porodice, nature, 7-day product",
         "Imas samo 3 dana ili zelis nightlife",
         "Tisi, priroda, plazo, farmhouse opcija",
         "Trajekt logistika, sporije sve",
         "Nije idealno",
         "High"],
    ]
    e.append(build_table(headers, rows,
                         col_widths=[2.8*cm, 3.2*cm, 3.2*cm, 3.2*cm, 2.5*cm, 1.3*cm, 1.3*cm]))
    e.append(PageBreak())
    return e

# ─── Section 4: Beaches ──────────────────────────────────────────────────────

def section4():
    e = []
    e.append(section_header("4", "Beaches"))
    e.append(sp(1))
    e.append(warn_box(
        "KLJUCNO: 'Seafront' NE znaci 'sandy beach'. Mnogi 'beachfront' hoteli imaju kamenitu obalu. "
        "Blue Lagoon: od 2025/2026 postoji QR/booking sistem za pristup obali — NE prodavati bez ovog warninga. "
        "Stene nisu za malu decu i slabe placace."
    ))
    e.append(sp(1))

    headers = ["Plaza", "Pesak / kamen", "Best for", "Pristup", "Glavni problem", "Conf."]
    rows = [
        ["Mellieha Bay / Ghadira",
         "Fini beli pesak",
         "Porodice, deca, slabi placaci (plitka voda)",
         "Odlican — bus direktno",
         "Ekstremna guzva jula/avgusta, komercijalno",
         "High"],
        ["Golden Bay",
         "Zlatni pesak",
         "Porodice, parovi, sunset",
         "Odlican — bus terminus",
         "Guzva, Radisson hotel dominira pogledom",
         "High"],
        ["Ghajn Tuffieha / Riviera",
         "Crvenkasto-zlatni pesak",
         "Parovi, fotografije, plivanje",
         "200 strmih stepenica — bus do vrha",
         "Struje/rip currents pri vetru, stepenice mobility problem",
         "High"],
        ["Gnejna Bay",
         "Zuti pesak, delom glina",
         "Parovi, lokalni vibz, manje guzve",
         "Slab bus iz Mgarra",
         "Desna strana = nezvanicna nudisticka plaza, bus redak",
         "Medium"],
        ["Paradise Bay",
         "Pesak, stepenice",
         "Parovi, plivanje, Gozo ferry combo",
         "15 min hoda od stopa uzbrdo",
         "Trajekt se vidi/cuje, guzva leti",
         "Medium"],
        ["St George's Bay (St Julian's)",
         "Pesak — mala urbana plaza",
         "Kratko kupanje, nightlife turisti",
         "Odlican",
         "Buka, komercijalno, ne najcistija",
         "Medium"],
        ["Blue Lagoon (Comino)",
         "Krec. kamen, minimalan pesak",
         "Parovi, fotografije, snorkeling",
         "Samo brodom iz Cirkewwe/Marfe",
         "GUZVA od 10–16h. QR/booking sistem za obalu. Nema hlada.",
         "High"],
        ["Ramla Bay (Gozo)",
         "Narandzasto-crveni pesak",
         "Porodice, parovi, fotografije",
         "Bus iz Viktorije (ne presto)",
         "Klizava kamena ploca na ulazu u vodu",
         "High"],
        ["St Peter's Pool",
         "Kamen — nema peska",
         "Plivaci, parovi, skokovi, fotografije",
         "30–40 min hoda od Marsaxlokka ili auto/taksi",
         "Nema hlada, izlaz samo merdevinama/skakanjem, nije za decu",
         "Medium"],
        ["Ghar Lapsi",
         "Kamen — prirodni pool",
         "Snorkeling, parovi",
         "Auto/bus 109 retko",
         "Otvoreno duboko more odmah, talasi, nema peska",
         "Medium"],
        ["Fond Ghadir / Sliema Roman Baths",
         "Kamen — rimski bazeni",
         "Kratko kupanje za smestene u Sliemi",
         "Odlican — na promenadi",
         "Duboko more odmah, talasi, nema peska za decu",
         "Medium"],
        ["Armier Bay",
         "Beli pesak",
         "Porodice, lokalni vibz",
         "Bus redak",
         "Vetar, improvizovane kucice kvare estetiku",
         "Medium"],
    ]
    e.append(build_table(headers, rows,
                         col_widths=[3.3*cm, 2.5*cm, 3.5*cm, 2.7*cm, 4*cm, 1.5*cm]))
    e.append(PageBreak())
    return e

# ─── Section 5: Hidden Gems ──────────────────────────────────────────────────

def section5():
    e = []
    e.append(section_header("5", "Hidden Gems — Top 12"))
    e.append(sp(1))

    gems = [
        {
            "name": "1. Wied il-Ghasri (Gozo)",
            "why": "Uska fjord-like klisura sa kristalnom vodom. Odlicno za snorkeling kada je more mirno.",
            "best": "Parovi, fotografija, snorkeling",
            "avoid": "Loso more, mala deca (teske stepenice)",
            "access": "Auto na Gozu, prateei put iz Marsalforna pored solana",
            "conf": "High",
            "source": "visitgozo.com"
        },
        {
            "name": "2. Tal-Mixta Cave (Gozo)",
            "why": "Prirodni 'prozor' iznad Ramla Bay — neverovatna perspektiva za fotografije.",
            "best": "Parovi, fotografi",
            "avoid": "Bez auta, vrelina, guzva",
            "access": "Auto na Gozu",
            "conf": "High",
            "source": "visitgozo.com"
        },
        {
            "name": "3. Fomm ir-Rih",
            "why": "Najdivlja i najizolovaniija uvala na Malti. Dramaticne bijele litice, tirkizna voda, potpuni mir.",
            "best": "Avanturisti, fit parovi, fotografi",
            "avoid": "Porodice, sandule, slaba kondicija, nocni povratak",
            "access": "Auto do Bahrije, zatim 20 min strmog silaska pesice",
            "conf": "High",
            "source": "visitmalta.com"
        },
        {
            "name": "4. Ghar Lapsi",
            "why": "Prirodni smaragdni bazen zastiteni stenama. Popularan medu lokalnim roniocima.",
            "best": "Parovi, snorkeling, fotografija",
            "avoid": "Vikendom (guzva lokalaca), talasi, trazenje peska",
            "access": "Auto juzno od Siggiewi; bus 109 retko",
            "conf": "High",
            "source": "visitmalta.com"
        },
        {
            "name": "5. Il-Maqluba (Qrendi)",
            "why": "Dzinovski prirodni sinkhole nastao 1317. Mikro-ekosistem, lokalna legenda.",
            "best": "Ljubitelji prirode/istorije/geologije",
            "avoid": "Beach-only dan",
            "access": "Auto ili bus do Qrendija, blizu kapele Sv. Mateja",
            "conf": "Medium",
            "source": "emalta.com"
        },
        {
            "name": "6. Victoria Lines / Bingemma",
            "why": "12km britanske odbrambene linije iz 19.v. — panoramski pogled na severni deo ostrva.",
            "best": "Hikeri, ljubitelji istorije, fotografija",
            "avoid": "Letnja podnevna vrucina, deca, slabija kondicija",
            "access": "Auto do Bingemma Gap ili bus do Mgarra pa pesice",
            "conf": "High",
            "source": "travel2malta.com"
        },
        {
            "name": "7. Buskett Gardens",
            "why": "Jedina prava suma na Malti — retka zelena oaza, nekadase loviste vitezova.",
            "best": "Porodice, parovi, piknik, alternativa za vruce dane",
            "avoid": "Zelis more taj dan",
            "access": "Auto ili bus blizu Mdine",
            "conf": "High",
            "source": "visitmalta.com"
        },
        {
            "name": "8. San Anton Gardens (Attard)",
            "why": "Botanicka basta oko predsednicke palate. Fontane, paunovi, hlad. Besplatno.",
            "best": "Porodice, parovi, rain/heat alternative",
            "avoid": "Zelis spektakularne coastal views",
            "access": "Bus ili auto, centralno",
            "conf": "High",
            "source": "visitmalta.com"
        },
        {
            "name": "9. Gozo Salt Pans (Xwejni)",
            "why": "Geometrijske solane uklesane u stene kod Marsalforna — ekstremno fotogenicno.",
            "best": "Fotografija, parovi, slow travel",
            "avoid": "Podnevna vrucina, nema hlada",
            "access": "Auto na Gozu, blizu Marsalforna",
            "conf": "High",
            "source": "visitgozo.com"
        },
        {
            "name": "10. Gardjola Gardens (Senglea)",
            "why": "Mali bastion viewpoint sa pogledom na Grand Harbour, Vallettu i Fort St Angelo.",
            "best": "Parovi, fotografija, blue hour, Three Cities tura",
            "avoid": "Zelis beach dan",
            "access": "Ferry ili dgħajsa do Three Cities, pesice u Senglei",
            "conf": "High",
            "source": "parksinmalta.mt"
        },
        {
            "name": "11. St Peter's Pool",
            "why": "Prirodni krec. bazen kod Marsaxlokka — dobar za skokove i fotografije.",
            "best": "Plivaci, parovi, fotografi",
            "avoid": "Mala deca, neplivaci, jako sunce, nema hlada",
            "access": "Auto/taksi preporuceno; 30-40 min pesice od Marsaxlokka",
            "conf": "Medium",
            "source": "maltainfoguide.com"
        },
        {
            "name": "12. Hal Saflieni Hypogeum",
            "why": "Podzemni UNESCO neolitski burial complex — jedinstven na svetu. Must za premium culture produkt.",
            "best": "History lovers, premium culture itinerary",
            "avoid": "Klaustrofobicni, last-minute bez karte (bukirati 3-4 meseca unapred!)",
            "access": "Bus ili auto do Paole",
            "conf": "High",
            "source": "heritagemalta.mt"
        },
    ]

    headers = ["Ime", "Zasto vazno", "Best for", "Avoid if", "Pristup", "Conf."]
    rows = []
    for g in gems:
        rows.append([g["name"], g["why"], g["best"], g["avoid"], g["access"], g["conf"]])

    e.append(build_table(headers, rows,
                         col_widths=[3.5*cm, 4.5*cm, 3*cm, 2.5*cm, 2.5*cm, 1.5*cm]))
    e.append(PageBreak())
    return e

# ─── Section 6: Romantic Spots ───────────────────────────────────────────────

def section6():
    e = []
    e.append(section_header("6", "Romantic Spots — Top 10"))
    e.append(sp(1))

    headers = ["Spot", "Najbolji termin", "Zasto romanticno", "Guzva", "Prakticna napomena"]
    rows = [
        ["Mdina noc (Silent City)",
         "Posle 21:00",
         "Uske ulice osvetljene fenjerima, tisina, iluzija proslosti",
         "Niska — grad zivi svoje ime noci",
         "Ulaz slobodan; dnevni izletnici odu do 20h"],
        ["Upper Barrakka Gardens",
         "Popodne / blue hour",
         "Najpoznatiji pogled na Grand Harbour i Three Cities",
         "Umerena (guzva oko gun salute u podne)",
         "Gun salute u 12:00 i 16:00; doci van tog termina"],
        ["Gardjola Gardens (Senglea)",
         "Kasno popodne / blue hour",
         "Intiman bastion sa jednim od najjacih harbour pogleda",
         "Minimalna",
         "Ukljuciti u Three Cities rutu; ferry + pesice"],
        ["Birgu Marina (Vittoriosa)",
         "Kasno uvece (22:00)",
         "Luksuzne jahte, odjaj svetla na vodi, diskretni vinski bari",
         "Niska",
         "Restoran Terrone — odlican za fine dining"],
        ["Spinola Bay (St Julian's)",
         "Noc",
         "Ribarski camci luzzu, 'LOVE' skulptura, odrazi svetla",
         "Prometna, ali atmosfera ostaje intimna",
         "Izbegavati direktnu blizinu Paceville zone"],
        ["Dingli Cliffs (kod kapele)",
         "Sat pre zalaska",
         "Dramatican west-coast sunset, otvoreni horizont mora",
         "Umerena",
         "Auto/taksi lakse; vetar moze biti jak — neprikladna obuca problem"],
        ["Ghajn Tuffieha — vrh iznad plaze",
         "Vreme zalaska",
         "360 pogled na zaliv i more, istorijska kula 17v.",
         "Umerena",
         "Bus do vrha, zatim kratak uspon; mobility issue = problem"],
        ["Three Cities dgħajsa crossing",
         "Tokom dana / uvece",
         "Tradicionalni camac prelazak preko Grand Harboura — premium micro-experience",
         "Niska",
         "Naplatuje se 2 EUR pp; kombinovati sa Gardjola Gardens"],
        ["Hastings Gardens (Valletta)",
         "Nakon zalaska, marina svetla",
         "Zaklonjeno od glavne guzve, pogled na Msida Creek marinu",
         "Retka — uglavnom lokalni parovi",
         "Manje poznat od Upper Barrakka — bolji za pravu intimnost"],
        ["Xlendi / Gozo",
         "Uvece",
         "Mala bay atmosfera, vecera pored mora, setnja uz stijene",
         "Niska",
         "Ukljuciti u overnight Gozo plan ili 7-day product"],
    ]
    e.append(build_table(headers, rows,
                         col_widths=[3.5*cm, 3*cm, 4.5*cm, 2.5*cm, 4*cm]))
    e.append(PageBreak())
    return e

# ─── Section 7: Sunset Spots ─────────────────────────────────────────────────

def section7():
    e = []
    e.append(section_header("7", "Sunset Spots — Top 8"))
    e.append(sp(1))

    headers = ["Spot", "Pristup", "Best za foto/parove", "Warning"]
    rows = [
        ["Dingli Cliffs",
         "Auto/taksi lako; bus 201 sporije",
         "Direktan sun-over-sea, epski kadar, odlican za parove",
         "Jak vetar; hodanje blizu ivice bez ograde"],
        ["Ghajn Tuffieha / Riviera",
         "Bus do vrha + 200 stepenica",
         "Kombinacija plaze + clay slopes + mora — najlepssi beach sunset",
         "Rip currents pri vetru; mobility issues za stepenice"],
        ["Golden Bay",
         "Odlican — bus terminus",
         "Laki pristup, dobra infrastruktura, porodice i parovi",
         "Guzva; Radisson hotel dominira pozadinom"],
        ["Dwejra Bay (Gozo)",
         "Auto ili bus iz Viktorije",
         "Dramaticne stene, Fungus Rock, tamno-zlatna svetlost",
         "Vise moguci jak vetar; Azure Window vise ne postoji (2017)"],
        ["Tal-Mixta Cave (Gozo)",
         "Auto na Gozu",
         "Prirodni okvir nad Ramla Bay — fotografski klasik",
         "Vrucina podne, guzva, bez auta ne ide lako"],
        ["Xwejni Salt Pans (Gozo)",
         "Auto na Gozu, blizu Marsalforna",
         "Geometrijske solane + more = odlicna tekstura za fotografije",
         "Vetar/talasi na samoj ivici; nema hlada"],
        ["Upper Barrakka / Valletta blue hour",
         "Pesice iz centra Vallette",
         "Harbour blue hour — nije direktan zalazak u more, ali je odlican",
         "Gost ne sme da ocekuje sunce koje pada u more — objasni razliku"],
        ["Gardjola Gardens (Senglea)",
         "Ferry + pesice u Three Cities",
         "Harbour lights ka Valletti; bolji blue hour nego klasican sea sunset",
         "Zelis direktan sun-over-sea — ovde nemas; kombinovati sa Dingli"],
    ]
    e.append(build_table(headers, rows,
                         col_widths=[3.5*cm, 3.5*cm, 5.5*cm, 5*cm]))
    e.append(PageBreak())
    return e

# ─── Section 8: Local Food ───────────────────────────────────────────────────

def section8():
    e = []
    e.append(section_header("8", "Lokalna hrana"))
    e.append(sp(1))

    e.append(subsection_bar("Sta obavezno probati"))
    food_rows = [
        ["Pastizzi", "Lisnato testo sa rikotom ili graškom. Jeftino, svuda dostupno. Apsolutni must.", "Svi", "High"],
        ["Stuffat tal-fenek (Fenkata)", "Nacionalno jelo — zeciji gulas u crvenom vinu. Meso spada sa kosti.", "Foodies, culture", "High"],
        ["Ftira / hobz biz-zejt", "Malteska pogaca sa tunjevinom, kaparima, paradajzom, maslinama, gbejna sirom.", "Svi, beach picnic", "Medium"],
        ["Lampuki pie", "Sezonska riba lampuki u piti — vise jesen/early summer.", "Foodies", "Medium"],
        ["Gbejna", "Lokalni sir, posebno Gozo; servira se sa paradajzom, kaparima, ftira.", "Foodies, Gozo", "Medium"],
        ["Bigilla", "Pasulj dip, obicno starter sa malteskin hlebom.", "Couples, families", "Medium"],
        ["Imqaret", "Przeni desert sa urmama — street food kod Vallette i festas.", "Slasticari", "Medium"],
        ["Kinnie / Cisk / lokalno vino", "Kinnie = gorka narandzasto piće, Cisk = lokalno pivo. Lokalna vina sve bolja.", "Svi", "Medium"],
    ]
    e.append(build_table(["Jelo", "Opis", "Za koga", "Conf."], food_rows,
                         col_widths=[3.5*cm, 7*cm, 4*cm, 3*cm]))
    e.append(sp(1))

    e.append(subsection_bar("Gde jesti — zone"))
    zone_rows = [
        ["Valletta", "Premium & fine dining. Merchant St, St Lucia St. Birate manje konobe u sporednim ulicama."],
        ["Marsaxlokk", "Riba i morski plodovi uz luku. NE ici nedjeljom (guzva/bazar). Ici u sredu/cetvrtak uvece."],
        ["Mgarr / Rabat", "Tradicijona kuhinja — zeciji gulas. Nize cene, ogromne porcije."],
        ["Gozo (Victoria / Xlendi / Marsalforn)", "Ftira, gbejna, morski plodovi. Lokalniji osecaj nego Malta mainland."],
        ["Sliema / St Julian's", "Prakticna turisticka zona. Veliki izbor, prosecni kvalitet."],
    ]
    e.append(build_table(["Zona", "Komentar"], zone_rows,
                         col_widths=[5*cm, 12.5*cm]))
    e.append(sp(1))

    e.append(warn_box(
        "IZBJEGAVATI: Restorani sa agresivnim hostovima, 'Tourist menu' za €15 (odmrznutl uvozni file), "
        "riba bez jasno navedene cene po grami, genericki talijanski meniji koji ne nude nista maltesko. "
        "Sveža lokalna riba uvek se naplacuje po kilogramu — ocekivati €25-30+ po osobi."
    ))
    e.append(PageBreak())
    return e

# ─── Section 9: What to Avoid ────────────────────────────────────────────────

def section9():
    e = []
    e.append(section_header("9", "Sta izbegavati — Top 15 Warninga"))
    e.append(sp(1))

    warns = [
        ["W1", "NE prodavati Maltu kao Maldives-style beach",
         "Vise od 50% obale je kamenita. Klijent ce biti razocaran i nazvati te. Uvek postavi ocekivanja."],
        ["W2", "NE slati porodice u Paceville",
         "Nightlife zona — buka do zore, pijanci, dzeparosi. Smestaj samo za party travellers."],
        ["W3", "NE preporucivati Blue Lagoon u podne jul/avg",
         "Katastrofalna guzva, brodovi ispustaju gasove, nema hlada, nema prostora. QR booking sistem je obavezan."],
        ["W4", "NE oslanjati se samo na bus za hidden beaches",
         "Za Fomm ir-Rih, St Peter's Pool, Gnejna, Ghar Lapsi — bus je redak ili ne postoji. Auto/taksi neophodan."],
        ["W5", "NE pretrpavati 3-day itinerary",
         "Malta izgleda mala, ali bus+saobracaj+vrucina usporavaju sve. Max 3 'stvari' po danu."],
        ["W6", "NE rezervovati hotel samo po 'distance to beach'",
         "300m do mora moze znaciti stene i beton, ne pesak. Uvek proveriti Google Maps satelit."],
        ["W7", "NE preskakati proveru recent recenzija",
         "Proveriti poslednjih 30-90 dana na Booking.com i TripAdvisor. Keywords: construction, drilling, crane, noise, AC."],
        ["W8", "Paziti na construction noise",
         "Malta je permanentno gradiliste. Hotel sa odlicnom prosecnom ocenom moze imati kran pored prozora."],
        ["W9", "Paziti na AC u ljetnom periodu",
         "Stare kamene zgrade akumuliraju toplotu. Bez funkcionalne klime leti = neizdrzivo. Uvek proveriti recenzije."],
        ["W10", "Paziti na 'real beach' vs 'rocky coast'",
         "Sliema, Gzira, Valletta, Three Cities = kamen, beton, rimski bazeni. Pesak je uglavnom na severu/sjeverozapadu."],
        ["W11", "Paziti na vetar, talase i crvene zastavice",
         "Golden Bay i Ghajn Tuffieha su osetljive na Majjistral (NW vetar) — struje postaju opasne."],
        ["W12", "NE ici u Marsaxlokk nedjeljom ako gost mrzi guzve",
         "Nedjeljni fish market je zapravo turisticki bazar. Preporuciti sredu/cetvrtak."],
        ["W13", "NE tretirati Gozo kao '2 sata usput'",
         "Gozo zasluzuje ceo dan. Dwejra, Ramla, Victoria, salt pans, Wied il-Ghasri = pun dan."],
        ["W14", "NE preporucivati cliff/pool spotove neplivacima",
         "St Peter's Pool, Ghar Lapsi, Wied il-Ghasri — nema lifeguarda, ulaz/izlaz samo skakanjem/merdevinama."],
        ["W15", "Hal Saflieni Hypogeum bez rane rezervacije",
         "Popularan, ulaznice se rasprodaju 3-4 meseca unapred. Last-minute ne radi."],
    ]
    e.append(build_table(["#", "Warning", "Detalj"], warns,
                         col_widths=[1*cm, 6*cm, 10.5*cm]))
    e.append(PageBreak())
    return e

# ─── Section 10: 3-Day Itinerary ─────────────────────────────────────────────

def section10():
    e = []
    e.append(section_header("10", "3-Day Itinerary (realan, nije pretrpan)"))
    e.append(sp(1))
    e.append(info_box("Tempo: 3 stavke max po danu. Uveci se preporuci setnja umesto dodavanja novih lokacija."))
    e.append(sp(1))

    # Day 1
    e.append(subsection_bar("Day 1: Valletta + Three Cities"))
    day1 = [
        ["Jutro", "Valletta: City Gate, Republic Street, St John's Co-Cathedral (bukirati unapred). "
                  "Upper Barrakka u 11:45 za gun salute u 12:00."],
        ["Podne/Popodne", "Barrakka Lift do pristanica. Dgħajsa prelazak (€2 pp) do Birgu/Vittoriosa. "
                          "Setnja marina, Fort St Angelo pogled, Gardjola Gardens u Senglei."],
        ["Uvece", "Povratak ferryjem u Vallettu. Vecera u sporednim ulicama blizu pijace. "
                  "Nocna setnja uz osvetljene zidine."],
        ["Rizici", "Letnja podnevna vrucina: Three Cities preporuciti za 15:00+. "
                   "Hotel daleko na sjeveru = kasni povratak bus problemom."],
    ]
    e.append(build_table(["Dio dana", "Plan"], day1,
                         col_widths=[3*cm, 14.5*cm]))
    e.append(sp(1))

    # Day 2
    e.append(subsection_bar("Day 2: Mdina/Rabat + Plaze + Zalazak"))
    day2 = [
        ["Jutro", "Mdina rano (prije turistickih grupa). Kafa u Fontanella baru sa pogledom na centralnu Maltu. "
                  "Setnja Mdinom."],
        ["Podne/Popodne", "Ručak u Rabatu (pastizzi u Crystal Palace ili tradicionaona konoba). "
                          "Odlazak na Golden Bay (laksak pristup, porodice) ili Ghajn Tuffieha (ljepsa, stepenice)."],
        ["Uvece", "Zalazak: Dingli Cliffs (auto/taksi preporuceno). Vecera u Rabatu — zeciji gulas."],
        ["Rizici", "Jak NW vetar = biraje Golden Bay umjesto Ghajn Tuffieha. "
                   "Ghajn Tuffieha stepenice = mobility problem za starije/djecu."],
    ]
    e.append(build_table(["Dio dana", "Plan"], day2,
                         col_widths=[3*cm, 14.5*cm]))
    e.append(sp(1))

    # Day 3
    e.append(subsection_bar("Day 3: Marsaxlokk + Jug Malte + Uvece Sliema/Spinola"))
    day3 = [
        ["Jutro", "Marsaxlokk: ribarska luka, setnja pored sarenih luzzu camaca. "
                  "NE ici nedjeljom ako gost mrzi guzve (bazar umjesto autenticnosti)."],
        ["Podne/Popodne", "St Peter's Pool (za plivace/avanturiste) ILI Blue Grotto viewpoint (za sve, "
                          "brodic ako more dozvoilava). Ručak u lokalu blizu."],
        ["Uvece", "Povratak u Sliemu ili St Julian's. Setnja promenadoim ili Spinola Bay. "
                  "Zavrsa vecera uz vodu."],
        ["Rizici", "St Peter's Pool: samo za dobre plivace. Auto/taksi neophodan. "
                   "Ako ostajete u Melliehi — adaptirati uvece na Melliehu village."],
    ]
    e.append(build_table(["Dio dana", "Plan"], day3,
                         col_widths=[3*cm, 14.5*cm]))
    e.append(PageBreak())
    return e

# ─── Section 11: 5-Day Itinerary ─────────────────────────────────────────────

def section11():
    e = []
    e.append(section_header("11", "5-Day Itinerary"))
    e.append(sp(1))
    e.append(info_box("Graditi na 3-day planu. Dodati: Comino rano, Gozo cijeli dan, juzna Malta/food dan."))
    e.append(sp(1))

    days = [
        ["Day 1", "Valletta + Three Cities", "Kao Day 1 u 3-day planu. Luksuznije opcije vecere."],
        ["Day 2", "Mdina/Rabat + Dingli zalazak", "Kultura + zalazak. Vecera sa rabbit u Rabatu."],
        ["Day 3", "Plaze — sjever/sjeverozapad", "Golden Bay ili Ghajn Tuffieha. Zalazak ako uvjeti dobri."],
        ["Day 4", "Gozo — cijeli dan", "Trajekt iz Cirkewwe. Victoria/Cittadella, Ramla Bay, Tal-Mixta Cave, "
                                       "sol pans ili Dwejra. Zalazak na Goz. Kasni trajekt nazad."],
        ["Day 5", "Juzna Malta + lokalna hrana", "Marsaxlokk (ne nedjeljom), St Peter's Pool ili Blue Grotto, "
                                                   "opciono Hagar Qim/Mnajdra hramovi. Vecera na moru."],
    ]
    e.append(build_table(["Dan", "Fokus", "Detalji"], days,
                         col_widths=[1.5*cm, 4*cm, 12*cm]))
    e.append(sp(1))
    e.append(Paragraph("Rizici: Gozo zahtijeva rani start. Blue Lagoon nije u 5-day planu — ako gost insistira, "
                        "ubaciti rano jutro Day 4 (08:00) prije Gozo ture.", sNote))
    e.append(PageBreak())
    return e

# ─── Section 12: 7-Day Itinerary ─────────────────────────────────────────────

def section12():
    e = []
    e.append(section_header("12", "7-Day Itinerary (Malta + Gozo + Comino)"))
    e.append(sp(1))

    days = [
        ["Day 1", "Valletta — sporiji dolazak",
         "Upper Barrakka, stare ulice, vecera u harbour zoni. Bez pretrpavanja."],
        ["Day 2", "Three Cities + Sliema ferry",
         "Birgu/Senglea ujutru/popodne. Ferry Valletta–Sliema za blue hour. Nocna setnja."],
        ["Day 3", "Mdina/Rabat + Dingli",
         "Silent City, lokalna hrana u Rabatu, Dingli Cliffs zalazak."],
        ["Day 4", "Sjeverne plaze",
         "Mellieha Bay (porodice) ili Golden/Ghajn Tuffieha (parovi). Alternativni bay pri lošem vetru."],
        ["Day 5", "Comino — Blue Lagoon",
         "ICI RANO (08:00, prvi brodic). QR booking/shore access obavezan. Napustiti do 11:30. "
         "Popodne odmor ili Paradise Bay."],
        ["Day 6", "Gozo — puni dan",
         "Dwejra, Inland Sea, Victoria/Cittadella, Ramla Bay/Tal-Mixta, sol pans. Zalazak na Gozu."],
        ["Day 7", "Juzna Malta + fleksibilan zavrsetak",
         "Marsaxlokk, St Peter's Pool/Blue Grotto, ili Hypogeum ako bukiran. Vecernji shopping/setnja."],
    ]
    e.append(build_table(["Dan", "Fokus", "Detalji"], days,
                         col_widths=[1.5*cm, 4*cm, 12*cm]))
    e.append(sp(1))
    e.append(subsection_bar("Alternativa za kisu / jak vetar / guzve"))
    e += bullets([
        "Valletta muzeji: National Museum of Archaeology, Lascaris War Rooms, St John's Co-Cathedral.",
        "San Anton Gardens (besplatno, pogodan za sve).",
        "Malta National Aquarium (Qawra) — odlicno za porodice.",
        "Esplora Interactive Science Centre (Kalkara) — porodice sa djecom.",
        "Mdina/Rabat unutrašnjost — crkve, konobe, setnja.",
        "Ako Western plaze zablokirane: preci na zastavicene bays prema istoku/jugu.",
    ])
    e.append(PageBreak())
    return e

# ─── Section 13: Hotel Booking Logic ─────────────────────────────────────────

def section13():
    e = []
    e.append(section_header("13", "Hotel Booking Logic"))
    e.append(sp(1))

    headers = ["Segment", "Najbolja zona", "Sta provjeriti", "Izbjegavati"]
    rows = [
        ["Porodice",
         "Mellieha, St Paul's Bay/Qawra",
         "Djejci bazen, lift, realna udaljenost do pescane plaze, velicina sobe",
         "Paceville, strme ulice Vallette, tiny boutique rooms"],
        ["Beach stay",
         "Mellieha Bay, Golden Bay resort zona, Paradise Bay/Marfa",
         "Da li je privatna plaza ili rocky coast, da li deckchairs ukljuceni",
         "Valletta, Gzira, Sliema ako gost trazi pesak"],
        ["Budget",
         "Gzira, Bugibba/Qawra, dijelovi Slieme",
         "Funkcionalna klima, pritisak vode, blizina bus terminusa",
         "Medeni mjesec, luxury ocekivanja"],
        ["Nightlife",
         "St Julian's / Paceville",
         "Zvucna izolacija (double-glazing), sigurnost u/oko hotela nocu",
         "Porodice, seniors, romantican odmor"],
        ["Parovi / romanticno",
         "Valletta boutique, Three Cities boutique, Mdina, Gozo farmhouse/Xlendi",
         "Krovni pogled, soba sa prozorom (ne atrijum), recenzije atmosfere",
         "Ako gost zeli resort beach only"],
        ["Luxury",
         "Valletta luxury boutique, St Julian's 5*, Gozo Kempinski",
         "Da li lido/bazen prodaju dnevne karte posjetiocima (guzva problem)",
         "Budget ocekivanja"],
    ]
    e.append(build_table(headers, rows,
                         col_widths=[3.5*cm, 4*cm, 6*cm, 4*cm]))
    e.append(PageBreak())
    return e

# ─── Section 14: Hotel QA Checklist ──────────────────────────────────────────

def section14():
    e = []
    e.append(section_header("14", "Manual Hotel QA Checklist"))
    e.append(sp(1))
    e.append(Paragraph("Prije nego agent preporuci hotel — proci kroz svaku tacku:", sH3))
    e.append(sp(1))

    checklist = [
        ["1", "Recent reviews (30–90 dana)", "Filtrirati na Booking.com i TripAdvisor — samo najnovije. Prosjecna ocena je lazepreci."],
        ["2", "Construction / buka", "Keywords u recenzijama: construction, drilling, crane, building site, noise, jackhammer."],
        ["3", "Status renoviranja", "'Recently renovated' provjeriti po sobama — ne samo lobby fotografije."],
        ["4", "Bazen otvoren / kapacitet", "Provjeriti: da li je otvoren u konkretnom mjesecu; da li se prodaju dnevne karte vanjskima."],
        ["5", "Realna udaljenost od plaze", "Google Maps satelit: da li vodi do pjescane plaze ili kamenite obale/promenade."],
        ["6", "AC u sezoni", "Ljeti je AC non-negotiable. Provjeri recenzije za 'no AC', 'broken AC', 'hot room'."],
        ["7", "Lift / pristupacnost", "Valletta/Three Cities/Mdina — stare zgrade bez lifta ceste. Provjeriti."],
        ["8", "Tacna ulica i buka", "St Julian's: razlika izmedju Spinola Bay (tiho) i 50m dalje u Paceville (kaos)."],
        ["9", "Gost fotografije vs hotel fotografije", "Sirokokutni objektiv cini bazen od 4m losim poput olimpijskog. Guest photos = realnost."],
        ["10", "Prevoz pristup", "Blizina bus linije, kasni nocni povratak, parking ako gost ima auto."],
        ["11", "Politika otkazivanja", "Peak sezona = skupa karta — free cancellation ili flexible rate preporuciti."],
    ]
    e.append(build_table(["#", "Stavka", "Detalj"], checklist,
                         col_widths=[0.8*cm, 4.2*cm, 12.5*cm]))
    e.append(PageBreak())
    return e

# ─── Section 15: Product Ideas ───────────────────────────────────────────────

def section15():
    e = []
    e.append(section_header("15", "Product Ideas za D&L Project56"))
    e.append(sp(1))

    headers = ["PDF Proizvod", "Target kupac", "Pain point", "Price idea", "Upsell"]
    rows = [
        ["Malta 3-Day Quick Plan",
         "First-timers, kratki odmor",
         "Ne znaju odakle krenuti, strahuju da nece stici nista",
         "€7–12",
         "Upgrade na 5-day plan"],
        ["Malta 5-Day Perfect Plan",
         "Parovi, porodice",
         "Zele balans plaze + kultura + Gozo — logistika nejasna",
         "€12–18",
         "Romantic ili Family add-on"],
        ["Malta Romantic Plan",
         "Parovi, godisnjice",
         "Gdje su pravi romanticni spotovi, zalasci, vecere",
         "€12–15",
         "Hotel area guide"],
        ["Malta Family Beach Plan",
         "Porodice sa malom djecom",
         "Koje plaze su bezbjedne, gdje smjestiti porodicu",
         "€10–15",
         "Hotel booking guide"],
        ["Malta Where to Stay Guide",
         "Svi segmenti, pre-booking",
         "Koja zona odgovara kakvom gostu",
         "€8–12",
         "Standalone ili bundle"],
        ["Malta Gozo + Comino Plan",
         "Island hopping fokus",
         "Logistika trajekta, Blue Lagoon timing, Gozo highlights",
         "€10–15",
         "7-day plan bundle"],
        ["Malta No-Car Itinerary",
         "Turisti bez auta",
         "Sta moze bez rent-a-cara, koje plaze su dostupne busom",
         "€8–12",
         "3 ili 5-day plan"],
        ["Malta Hotel Area Mistakes Guide",
         "Pre-booking faza",
         "Kako ne knjiziti hotel u pogresnoj zoni, sta provjeriiti",
         "€6–9",
         "Where to Stay Guide"],
    ]
    e.append(build_table(headers, rows,
                         col_widths=[4.5*cm, 3*cm, 4.5*cm, 2*cm, 3.5*cm]))
    e.append(sp(1))
    e.append(Paragraph("Napomena: Sve price ideas su orijentacione — nisu verifikovane trzisno. Oznacene su kao 'price idea'.", sNote))
    e.append(PageBreak())
    return e

# ─── Section 16: Lejla Approval ──────────────────────────────────────────────

def section16():
    e = []
    # Distinctive approval header
    header_data = [[Paragraph("16.  LEJLA — REVIEW &amp; APPROVAL", sH1)]]
    ht = Table(header_data, colWidths=[17.5*cm])
    ht.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), ORANGE),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
    ]))
    e.append(ht)
    e.append(sp(2))

    e.append(Paragraph(
        "Ovaj dokument je spreman za tvoj pregled. Procitaj, oznaci odgovore i vrati feedback. "
        "Nijedan PDF proizvod ne ide u produkciju dok ne dobijem tvoje odobrenje.",
        sApproval))
    e.append(sp(2))

    e.append(HRFlowable(width="100%", thickness=1, color=ORANGE))
    e.append(sp(1))

    questions = [
        {
            "num": "1",
            "q": "Da li je Malta dobar prvi paid PDF travel product?",
            "options": ["Da — krecemo", "Da, ali treba jos istrazivanja", "Ne — biraj drugu destinaciju"]
        },
        {
            "num": "2",
            "q": "Koji segment gađamo PRVI?",
            "options": ["Parovi", "Porodice", "First-time Malta (general)", "No-car travellers"]
        },
        {
            "num": "3",
            "q": "Da li idemo sa 3/5/7 day PDF paketima?",
            "options": ["Da — sva tri", "Samo 3 i 5 day", "Kreni sa jednim (naznaci kojim)", "Drugacija struktura"]
        },
        {
            "num": "4",
            "q": "Da li prvo pravimo jedan premium PDF ili vise manjih?",
            "options": ["Jedan sveobuhvatni premium PDF", "Vise manjnih po segmentu", "Bundle paket (3 u 1)"]
        },
        {
            "num": "5",
            "q": "Da li se slazs da Blue Lagoon i hotel-zone warnings budu jako naglaseni?",
            "options": ["Da — jako naglasiti", "Umjereno — ne plasiti klijente", "Preformulisati neutral"]
        },
        {
            "num": "6",
            "q": "Finalna ocjena dokumenta",
            "options": ["APPROVED — krecemo u produkciju", "NEEDS CHANGES — detaljise napomene ispod",
                        "REJECT — objasni razlog"]
        },
    ]

    for q in questions:
        q_data = [[Paragraph(f"Pitanje {q['num']}: {q['q']}",
                             S("qh", fontSize=10, fontName="Helvetica-Bold",
                               textColor=DARK_NAVY, leading=14))]]
        qt = Table(q_data, colWidths=[17.5*cm])
        qt.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), LIGHT_BLUE),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("LINEBELOW", (0,0), (-1,-1), 1, MID_BLUE),
        ]))
        e.append(qt)
        for opt in q["options"]:
            opt_data = [[
                Paragraph("[ ]", S("cb", fontSize=10, fontName="Helvetica",
                                   textColor=MID_BLUE, leading=13)),
                Paragraph(opt, sApproval)
            ]]
            ot = Table(opt_data, colWidths=[0.8*cm, 16.7*cm])
            ot.setStyle(TableStyle([
                ("TOPPADDING",    (0,0), (-1,-1), 3),
                ("BOTTOMPADDING", (0,0), (-1,-1), 3),
                ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ]))
            e.append(ot)
        e.append(sp(1))

    e.append(sp(1))
    e.append(HRFlowable(width="100%", thickness=1, color=ORANGE))
    e.append(sp(1))

    notes_data = [[Paragraph("Napomene / Komentari Lejle:", S("nl",
                    fontSize=10, fontName="Helvetica-Bold",
                    textColor=DARK_NAVY, leading=13))]]
    notes_box = Table([
        notes_data[0],
        [[Paragraph(" " * 200 + "\n\n\n\n\n\n\n\n", sBody)]],
    ], colWidths=[17.5*cm])
    notes_box.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 1, MID_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("BACKGROUND", (0,0), (0,0), LIGHT_BLUE),
        ("LINEBELOW", (0,0), (0,0), 0.5, MID_BLUE),
    ]))
    e.append(notes_box)
    e.append(sp(2))

    footer_data = [[Paragraph(
        "D&amp;L Project56 — Malta Travel Product Pool | Internal Review v1.0 | 26.06.2026. | "
        "INTERNO — Nije za distribuciju klijentima",
        S("f", fontSize=7, textColor=colors.HexColor("#888888"),
          fontName="Helvetica", alignment=TA_CENTER, leading=10))]]
    ft = Table(footer_data, colWidths=[17.5*cm])
    ft.setStyle(TableStyle([
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("LINEABOVE", (0,0), (-1,-1), 0.5, MED_GREY),
    ]))
    e.append(ft)
    return e

# ─── Page template ────────────────────────────────────────────────────────────

def on_page(canvas, doc):
    canvas.saveState()
    page_num = canvas.getPageNumber()
    if page_num > 1:  # skip cover
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#888888"))
        canvas.drawRightString(
            A4[0] - 1.5*cm,
            0.8*cm,
            f"D&L Project56 — Malta Internal Review v1.0 | Strana {page_num}"
        )
        canvas.setStrokeColor(MED_GREY)
        canvas.setLineWidth(0.3)
        canvas.line(1.5*cm, 1.2*cm, A4[0] - 1.5*cm, 1.2*cm)
    canvas.restoreState()

# ─── Main ─────────────────────────────────────────────────────────────────────

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.8*cm,
        title="D&L Project56 — Malta Travel Product Internal Review",
        author="D&L Project56 AI Engine",
        subject="Internal Product Review for Lejla",
    )

    story = []
    story += cover_page()
    story += toc_page()
    story += section1()
    story += section2()
    story += section3()
    story += section4()
    story += section5()
    story += section6()
    story += section7()
    story += section8()
    story += section9()
    story += section10()
    story += section11()
    story += section12()
    story += section13()
    story += section14()
    story += section15()
    story += section16()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF generated: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
