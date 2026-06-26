#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D&L Project56 — Malta Travel Product Internal Review PDF
Version: 1.1  (language polish + encoding fix)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER

OUTPUT_PATH = "/home/user/dejan/DL_Project56_Malta_Travel_Product_Internal_Review_v1_1.pdf"

# ── Boje ──────────────────────────────────────────────────────────────────────
DARK_NAVY  = colors.HexColor("#1A2340")
MID_BLUE   = colors.HexColor("#2E4A7A")
LIGHT_BLUE = colors.HexColor("#E8EDF5")
ORANGE     = colors.HexColor("#C8521A")
LIGHT_GREY = colors.HexColor("#F4F4F4")
MED_GREY   = colors.HexColor("#CCCCCC")
RED_WARN   = colors.HexColor("#C0392B")
GREEN_OK   = colors.HexColor("#1E7B4B")
WHITE      = colors.white
BLACK      = colors.black

# ── Stilovi ───────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle   = S("sTitle",   fontSize=22, leading=28, textColor=WHITE,
             fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
sSub     = S("sSub",     fontSize=11, leading=14, textColor=colors.HexColor("#BDC8E0"),
             fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
sH1      = S("sH1",      fontSize=15, leading=20, textColor=WHITE,
             fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=4)
sH2      = S("sH2",      fontSize=12, leading=16, textColor=DARK_NAVY,
             fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4)
sH3      = S("sH3",      fontSize=10, leading=13, textColor=MID_BLUE,
             fontName="Helvetica-Bold", spaceBefore=5, spaceAfter=3)
sBody    = S("sBody",    fontSize=9,  leading=13, textColor=BLACK,
             fontName="Helvetica", spaceBefore=2, spaceAfter=2)
sSmall   = S("sSmall",   fontSize=8,  leading=11, textColor=colors.HexColor("#333333"),
             fontName="Helvetica", spaceBefore=1, spaceAfter=1)
sWarn    = S("sWarn",    fontSize=9,  leading=12, textColor=RED_WARN,
             fontName="Helvetica-Bold", spaceBefore=2, spaceAfter=2)
sNote    = S("sNote",    fontSize=8,  leading=11, textColor=colors.HexColor("#555555"),
             fontName="Helvetica-Oblique", spaceBefore=1, spaceAfter=1)
sBullet  = S("sBullet",  fontSize=9,  leading=12, textColor=BLACK,
             fontName="Helvetica", leftIndent=12, spaceBefore=1, spaceAfter=1,
             bulletIndent=4)
sTOC     = S("sTOC",     fontSize=9,  leading=13, textColor=MID_BLUE,
             fontName="Helvetica", spaceBefore=1, spaceAfter=1)
sApprove = S("sApprove", fontSize=10, leading=14, textColor=DARK_NAVY,
             fontName="Helvetica", spaceBefore=3, spaceAfter=3)

# ── Pomocne funkcije ──────────────────────────────────────────────────────────

def sp(n=1):
    return Spacer(1, n * 0.25 * cm)

def sec_hdr(num, text):
    label = f"{num}.  {text}" if num else text
    t = Table([[Paragraph(label, sH1)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), DARK_NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return t

def sub_hdr(text):
    t = Table([[Paragraph(text, sH2)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("LINEBELOW",     (0,0), (-1,-1), 1, MID_BLUE),
    ]))
    return t

def warn_box(text):
    t = Table([[Paragraph(text, sWarn)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#FEF0ED")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 1, RED_WARN),
    ]))
    return t

def info_box(text):
    t = Table([[Paragraph(text, sBody)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#EBF5EB")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 1, GREEN_OK),
    ]))
    return t

def tbl(headers, rows, col_widths=None):
    th_style = S("th", fontSize=8, fontName="Helvetica-Bold",
                 textColor=WHITE, leading=11)
    data = [[Paragraph(h, th_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), sSmall) for c in row])
    if col_widths is None:
        w = 17.5 * cm / len(headers)
        col_widths = [w] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), MID_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("GRID",          (0,0), (-1,-1), 0.4, MED_GREY),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
    ]))
    return t

def bul(items):
    return [Paragraph(f"<bullet>&bull;</bullet> {i}", sBullet) for i in items]

# ── Naslovnica ────────────────────────────────────────────────────────────────

def cover():
    e = [Spacer(1, 3*cm)]
    tb = Table([
        [Paragraph("D&amp;L Project56", sSub)],
        [Paragraph("MALTA TRAVEL PRODUCT POOL", sTitle)],
        [Paragraph("Internal Review Version for Lejla", sSub)],
        [Paragraph("Datum: 26. juni 2026.  |  Verzija: 1.1  |  Status: DRAFT — CEKA ODOBRENJE", sSub)],
    ], colWidths=[17.5*cm])
    tb.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), DARK_NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 11),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("LEFTPADDING",   (0,0), (-1,-1), 18),
    ]))
    e.append(tb)
    e.append(sp(3))
    meta = [
        ["Dokument",         "DL_Project56_Malta_Travel_Product_Internal_Review_v1_1.pdf"],
        ["Priprema",         "D&L Project56 — AI Research Engine"],
        ["Namena",           "Interni approval pregled — nije za klijente"],
        ["Izvor materijala", "3 research bloka spojena bez dupliranja"],
        ["Jezik",            "Srpski / balkanski, direktan poslovni stil"],
    ]
    mt = Table(meta, colWidths=[5*cm, 12.5*cm])
    mt.setStyle(TableStyle([
        ("FONTNAME",      (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",      (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("LEADING",       (0,0), (-1,-1), 13),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("GRID",          (0,0), (-1,-1), 0.3, MED_GREY),
        ("ROWBACKGROUNDS",(0,0), (-1,-1), [WHITE, LIGHT_GREY]),
    ]))
    e.append(mt)
    e.append(sp(3))
    e.append(warn_box(
        "INTERNO — nije za klijente. Sadrzi konkretan research, operativne smernice i "
        "preporuke za razvoj proizvoda. Lejla treba da procita, obeli stavke i vrati "
        "feedback pre pokretanja produkcije bilo kojeg PDF proizvoda."
    ))
    e.append(PageBreak())
    return e

# ── Sadrzaj ───────────────────────────────────────────────────────────────────

def toc():
    e = [sec_hdr("", "Sadrzaj"), sp(1)]
    items = [
        ("1.",  "Executive Summary"),
        ("2.",  "Malta Positioning — sta prodavati i kako"),
        ("3.",  "Best Areas to Stay — tabele po zoni"),
        ("4.",  "Plaze — tabela"),
        ("5.",  "Hidden Gems — top 12"),
        ("6.",  "Romanticni spotovi — top 10"),
        ("7.",  "Zalasci sunca — top 8"),
        ("8.",  "Lokalna hrana"),
        ("9.",  "Sta izbegavati — top 15 upozorenja"),
        ("10.", "3-Day Itinerary"),
        ("11.", "5-Day Itinerary"),
        ("12.", "7-Day Itinerary"),
        ("13.", "Hotel Booking Logic"),
        ("14.", "Manual Hotel QA Checklist"),
        ("15.", "Product Ideas za D&L Project56"),
        ("16.", "LEJLA — Review & Approval"),
    ]
    for num, title in items:
        row = Table([
            [Paragraph(num, S("tn", fontSize=9, fontName="Helvetica-Bold",
                               textColor=MID_BLUE, leading=13)),
             Paragraph(title, sTOC)]
        ], colWidths=[1.2*cm, 16.3*cm])
        row.setStyle(TableStyle([
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LINEBELOW",     (0,0), (-1,-1), 0.3, MED_GREY),
        ]))
        e.append(row)
    e.append(PageBreak())
    return e

# ── Sekcija 1: Executive Summary ──────────────────────────────────────────────

def s1():
    e = [sec_hdr("1", "Executive Summary"), sp(1)]

    e.append(sub_hdr("Zasto Malta ima smisla kao travel product"))
    e += bul([
        "Kompaktna destinacija: celo ostrvo prelazis za manje od 1h — lako za planiranje 3-7 dana.",
        "Vise od 300 suncanih dana godisnje; more toplo od juna do oktobra.",
        "UNESCO trojka: Valletta, Megalitski hramovi, Hal Saflieni Hypogeum.",
        "Kombinacija istorije + mora + island hoppinga = visoka percipirana vrednost za paket.",
        "Razvijen ferry sistem (Sliema-Valletta, Valletta-Three Cities, Malta-Gozo).",
        "Turisticki segment dominantno mid-range + parovi + porodice = direktna ciljna publika D&L.",
        "Jak USP: sunset spotovi, romanticne lokacije, hidden gems — dobro se prodaje.",
    ])
    e.append(sp(1))

    e.append(sub_hdr("Za koga je Malta dobra"))
    e += bul([
        "Parovi — zalasci, vecere, male distance, romanticni stari gradovi.",
        "First-time travelers — bez logistickog stresa, sve blizu, engleski svuda.",
        "Kratki odmori 3-5 dana.",
        "City-break + more kombinacija.",
        "Porodice sa starijom decom — planerske aktivnosti + plaze.",
        "Ljubitelji istorije, fotografije i gastronomije.",
    ])
    e.append(sp(1))

    e.append(sub_hdr("Za koga Malta NIJE dobra"))
    e += bul([
        "Turisti koji ocekuju duge pescane plaze kao Grcka ili Turska — vise od 50% obale je kamenita.",
        "All-inclusive resort vibe — ne postoji u tom formatu.",
        "Porodice sa bebama u kolicima — strme ulice i kamene stepenice u Valletti i Mdini.",
        "Klijenti koji ne podnose guzvu u julu/avgustu.",
        "Oni koji traze potpunu tisinu i izolaciju.",
        "Klijenti sa smanjenom pokretljivoscu — topografija je zahtevna.",
    ])
    e.append(sp(1))

    e.append(sub_hdr("Najbolji meseci"))
    rows = [
        ["Maj (kraj) / Juni",       "ODLICNO",              "Balans temperature, manje guzve, nize cene"],
        ["Juli / Avgust",           "DOBRO za more — TESKO inace", "38-40°C + vlaga, najvece guzve, skuplje"],
        ["Septembar / Oktobar",     "ODLICNO",              "More jos toplo, guzve manje, prijatnija temperatura"],
        ["April / rani Maj",        "DOBRO",                "Hladnije, kulturne ture, ne za plazu"],
        ["Novembar - Mart",         "NIJE za plazu",        "Tura destinacija, ne letovalisni segment"],
    ]
    e.append(tbl(["Mesec", "Ocena", "Napomena"], rows,
                 col_widths=[4.5*cm, 4.5*cm, 8.5*cm]))
    e.append(sp(1))

    e.append(sub_hdr("Glavni rizici"))
    risks = [
        ["Guzva u avgustu",         "Blue Lagoon, Golden Bay, bus linije — katastrofalno pretrpano"],
        ["Prevoz bez auta",         "Bus je spor i leti pretrpan; hidden beaches bez auta su problem"],
        ["Pogresna zona smestaja",  "300m do mora moze znaciti stene, ne pesak"],
        ["Blue Lagoon bez bookinga","Od 2025/2026: QR/booking sistem za pristup obali — mora se planirati unapred"],
        ["Premalo peska",           "Vise od 50% obale je kamenita; klijenti moraju znati pre bookinga"],
        ["Construction buka",       "Malta je gradiliste; hotel bez provere poslednjih 30-90 recenzija = rizik"],
    ]
    e.append(tbl(["Rizik", "Objasnjenje"], risks, col_widths=[5*cm, 12.5*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 2: Positioning ────────────────────────────────────────────────────

def s2():
    e = [sec_hdr("2", "Malta Positioning — sta prodavati i kako"), sp(1)]
    e.append(warn_box(
        "NE prodavati Maltu kao 'pure beach resort'. Klijenti ce biti razocaran. "
        "Prodavati kao: more + istorija + island hopping + romanticni spotovi + hrana + zalasci."
    ))
    e.append(sp(1))
    e.append(sub_hdr("Idealni PDF proizvodi"))
    rows = [
        ["Malta 3-Day Quick Plan",        "First-timers, kratki odmor",       "Ne znaju odakle krenuti, boje se da nece stici nista"],
        ["Malta 5-Day Perfect Plan",      "Parovi, porodice",                 "Zele balans plaze + kultura + Gozo, ali ne znaju logistiku"],
        ["Malta 7-Day Full Plan",         "Duzi odmor, drugi put na Malti",   "Gozo + Comino + jug Malte + slobodan beach dan"],
        ["Romantic Malta PDF",            "Parovi, godisnjice",               "Gde su pravi romanticni spotovi, zalasci, vecere"],
        ["Family Beach Malta PDF",        "Porodice sa decom",                "Koje su prave pescane plaze, sta je bezbedno za decu"],
        ["Where to Stay in Malta Guide",  "Svi segmenti",                     "Koja zona je dobra za kog gosta — bez skupih gresaka"],
        ["Malta No-Car Itinerary",        "Turisti bez auta",                 "Sta moze bez rent-a-cara, koje plaze su dostupne busom"],
        ["Malta Hotel Area Mistakes Guide","Pre-booking faza",                "Kako ne rezervisati hotel u pogresnoj zoni"],
        ["Malta Gozo + Comino Plan",      "Island hopping fokus",             "Logistika trajekta, timing Blue Lagoon, Gozo highlights"],
    ]
    e.append(tbl(["Naziv", "Target", "Pain point koji resava"], rows,
                 col_widths=[5*cm, 4.5*cm, 8*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 3: Areas to Stay ──────────────────────────────────────────────────

def s3():
    e = [sec_hdr("3", "Best Areas to Stay"), sp(1)]
    e.append(Paragraph(
        "Napomena: 'seafront hotel' ne znaci 'beachfront hotel'. Mnogi hoteli uz more imaju kamenitu obalu "
        "ili betonsku promenadu. Uvek proveriti Google Maps satelit pre preporuke.",
        sNote))
    e.append(sp(1))
    headers = ["Area", "Best for", "Avoid if", "Pros", "Cons", "Bez auta?", "Conf."]
    rows = [
        ["Valletta",
         "First-timers, parovi, 3 dana, kultura",
         "Zelis plazu ili nightlife",
         "Walkable, UNESCO, restorani, ferry, logistika",
         "Nema plaze, skuplje, tiho nocu",
         "Da — idealna",
         "High"],
        ["Sliema / Gzira",
         "Parovi, porodice starija deca, mid-range",
         "Trazis pescanu plazu ispred hotela",
         "Promenada, restorani, ferry, shopping, prevoz",
         "Nema pescane plaze (rocky coast), buka saobracaja",
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
         "Party travelers",
         "Parovi, porodice, seniors, miran odmor",
         "Klubovi, barovi",
         "Buka do zore, guzva, manje bezbedno noci",
         "Da",
         "High"],
        ["Mellieha",
         "Porodice, beach-first odmor",
         "Zelis Vallettu svaki dan bez auta",
         "Najveca pescana plaza, Gozo ferry blizu",
         "Daleko od centra, bus leti pretrpan",
         "Moze, treba strpljenje",
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
         "Autentican ambijent, harbour views, ferry za Vallettu",
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
         "Parovi, porodice, priroda, 7-day product",
         "Imas samo 3 dana ili zelis nightlife",
         "Tise, priroda, plaze, farmhouse opcija",
         "Trajekt logistika, sporiji tempo",
         "Nije idealno",
         "High"],
    ]
    e.append(tbl(headers, rows,
                 col_widths=[2.8*cm, 3.2*cm, 3.2*cm, 3.2*cm, 2.5*cm, 1.3*cm, 1.3*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 4: Plaze ─────────────────────────────────────────────────────────

def s4():
    e = [sec_hdr("4", "Plaze"), sp(1)]
    e.append(warn_box(
        "KLJUCNO: 'Seafront' NE znaci 'sandy beach'. Mnogi 'beachfront' hoteli imaju kamenitu obalu. "
        "Blue Lagoon: od 2025/2026 postoji QR/booking sistem za pristup obali — NE prodavati bez ovog upozorenja. "
        "Stene nisu za malu decu i slabe plivace."
    ))
    e.append(sp(1))
    headers = ["Plaza", "Pesak / kamen", "Best for", "Pristup", "Glavni problem", "Conf."]
    rows = [
        ["Mellieha Bay / Ghadira",
         "Fini beli pesak",
         "Porodice, deca, slabi plivaci (plitka voda)",
         "Odlican — bus direktno",
         "Ekstremna guzva jula/avgusta, komercijalno",
         "High"],
        ["Golden Bay",
         "Zlatni pesak",
         "Porodice, parovi, zalazak",
         "Odlican — bus terminus",
         "Guzva, Radisson hotel dominira pogledom",
         "High"],
        ["Ghajn Tuffieha / Riviera",
         "Crvenkasto-zlatni pesak",
         "Parovi, fotografije, plivanje",
         "200 strmih stepenica — bus do vrha",
         "Struje pri vetru, stepenice = mobility problem",
         "High"],
        ["Gnejna Bay",
         "Zuti pesak, delom glina",
         "Parovi, lokalni vibe, manje guzve",
         "Slab bus iz Mgarra",
         "Bus redak; desna strana nezvano za nudiste",
         "Medium"],
        ["Paradise Bay",
         "Pesak, stepenice",
         "Parovi, plivanje, Gozo ferry combo",
         "15 min hoda uzbrdo od stopa",
         "Trajekt se vidi i cuje, guzva leti",
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
         "GUZVA od 10-16h. QR/booking sistem za obalu. Nema hlada.",
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
         "30-40 min pesice od Marsaxlokka ili auto/taksi",
         "Nema hlada, izlaz samo merdevinama/skakanjem, nije za decu",
         "Medium"],
        ["Ghar Lapsi",
         "Kamen — prirodni pool",
         "Snorkeling, parovi",
         "Auto / bus 109 retko",
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
         "Porodice, lokalni vibe",
         "Bus redak",
         "Vetar, improvizovane kucice kvare estetiku",
         "Medium"],
    ]
    e.append(tbl(headers, rows,
                 col_widths=[3.3*cm, 2.5*cm, 3.3*cm, 2.7*cm, 4.2*cm, 1.5*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 5: Hidden Gems ────────────────────────────────────────────────────

def s5():
    e = [sec_hdr("5", "Hidden Gems — Top 12"), sp(1)]
    gems = [
        ["1. Wied il-Ghasri (Gozo)",
         "Uska fjord-like klisura sa kristalnom vodom. Odlicno za snorkeling kada je more mirno.",
         "Parovi, fotografija, snorkeling",
         "Lose more, mala deca (teske stepenice)",
         "Auto na Gozu, put iz Marsalforna pored solana",
         "High"],
        ["2. Tal-Mixta Cave (Gozo)",
         "Prirodni 'prozor' iznad Ramla Bay — neverovatna perspektiva za fotografije.",
         "Parovi, fotografi",
         "Bez auta, vreline, guzva",
         "Auto na Gozu",
         "High"],
        ["3. Fomm ir-Rih",
         "Najdivlja i najizolovaniija uvala na Malti. Dramaticne bele litice, tirkizna voda, potpuni mir.",
         "Avanturisti, fit parovi, fotografi",
         "Porodice, sandale, slaba kondicija, nocni povratak",
         "Auto do Bahrije, zatim 20 min strmog silaska pesice",
         "High"],
        ["4. Ghar Lapsi",
         "Prirodni smaragdni bazen zastiteni stenama. Popularan medu lokalnim roniocima.",
         "Parovi, snorkeling, fotografija",
         "Vikendom — guzva lokalaca; talasi; trazenje peska",
         "Auto juzno od Siggiewi; bus 109 retko",
         "High"],
        ["5. Il-Maqluba (Qrendi)",
         "Ogromni prirodni sinkhole nastao 1317. Mikro-ekosistem, lokalna legenda.",
         "Ljubitelji prirode, istorije, geologije",
         "Beach-only dan",
         "Auto ili bus do Qrendija, blizu kapele Sv. Mateja",
         "Medium"],
        ["6. Victoria Lines / Bingemma",
         "12km britanskih odbrambenih zidova iz 19.v. — panoramski pogled na severni deo ostrva.",
         "Hikeri, ljubitelji istorije, fotografija",
         "Letnja podnevna vrucina, deca, slabija kondicija",
         "Auto do Bingemma Gap ili bus do Mgarra pa pesice",
         "High"],
        ["7. Buskett Gardens",
         "Jedina prava suma na Malti — retka zelena oaza, nekadanje loviste vitezova.",
         "Porodice, parovi, piknik, alternativa za vrue dane",
         "Zelis more taj dan",
         "Auto ili bus, blizu Mdine",
         "High"],
        ["8. San Anton Gardens (Attard)",
         "Botanicka basta oko predsednicke palate. Fontane, paunovi, hlad. Besplatno.",
         "Porodice, parovi, rain/heat alternativa",
         "Zelis spektakularne coastal views",
         "Bus ili auto, centralno",
         "High"],
        ["9. Gozo Salt Pans (Xwejni)",
         "Geometrijske solane uklesane u stene kod Marsalforna — ekstremno fotogenicno.",
         "Fotografija, parovi, slow travel",
         "Podnevna vrucina, nema hlada",
         "Auto na Gozu, blizu Marsalforna",
         "High"],
        ["10. Gardjola Gardens (Senglea)",
         "Mali bastion viewpoint sa pogledom na Grand Harbour, Vallettu i Fort St Angelo.",
         "Parovi, fotografija, blue hour, Three Cities ruta",
         "Zelis beach dan",
         "Ferry ili tradicional. camac do Three Cities, pesice u Senglei",
         "High"],
        ["11. St Peter's Pool",
         "Prirodni krecnjacki bazen kod Marsaxlokka — dobar za skokove i fotografije.",
         "Plivaci, parovi, fotografi",
         "Mala deca, neplivaci, jako sunce, nema hlada",
         "Auto/taksi preporuceno; 30-40 min pesice od Marsaxlokka",
         "Medium"],
        ["12. Hal Saflieni Hypogeum",
         "Podzemni UNESCO neolitski burial complex — jedinstven na svetu. Must za premium culture produkt.",
         "History lovers, premium culture itinerary",
         "Klaustrofobicni; last-minute bez karte (bukirati 3-4 meseca unapred!)",
         "Bus ili auto do Paole",
         "High"],
    ]
    e.append(tbl(
        ["Ime", "Zasto vazno", "Best for", "Avoid if", "Pristup", "Conf."],
        gems,
        col_widths=[3.5*cm, 4.5*cm, 3*cm, 2.5*cm, 2.5*cm, 1.5*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 6: Romanticni spotovi ────────────────────────────────────────────

def s6():
    e = [sec_hdr("6", "Romanticni spotovi — Top 10"), sp(1)]
    rows = [
        ["Mdina noc (Silent City)",
         "Posle 21:00",
         "Uske ulice osvetljene fenjerima, tisina, iluzija proslosti. Dnevni turisti su otisli.",
         "Niska",
         "Ulaz slobodan; dnevni izletnici odu do 20h"],
        ["Upper Barrakka Gardens",
         "Popodne / blue hour",
         "Najpoznatiji pogled na Grand Harbour i Three Cities",
         "Umerena (guzva oko gun salute u podne)",
         "Gun salute u 12:00 i 16:00; doci van tog termina"],
        ["Gardjola Gardens (Senglea)",
         "Kasno popodne / blue hour",
         "Intiman bastion sa jednim od najjacih harbour pogleda na Malti",
         "Minimalna",
         "Ukljuciti u Three Cities rutu; ferry + pesice"],
        ["Birgu Marina (Vittoriosa)",
         "Kasno uvece (22:00)",
         "Luksuzne jahte, odrazi svetla na vodi, diskretni vinski barovi u starim skladistima",
         "Niska",
         "Restoran Terrone — dobar za fine dining"],
        ["Spinola Bay (St Julian's)",
         "Noc",
         "Ribarski camci luzzu, 'LOVE' skulptura, odrazi svetla na vodi",
         "Prometna, ali atmosfera ostaje intimna",
         "Izbegavati direktnu blizinu Paceville zone"],
        ["Dingli Cliffs (kod kapele)",
         "Sat pre zalaska",
         "Dramatican west-coast zalazak, otvoreni horizont mora",
         "Umerena",
         "Auto/taksi lakse; vetar moze biti jak — neprikladna obuca problem"],
        ["Ghajn Tuffieha — vrh iznad plaze",
         "Vreme zalaska",
         "360-stepeni pogled na zaliv i more, istorijska kula iz 17. veka",
         "Umerena",
         "Bus do vrha, zatim kratak uspon; mobility issue = problem"],
        ["Three Cities — prelazak camcem",
         "Tokom dana / uvece",
         "Tradicional. camac (dghajsa) prelazak preko Grand Harboura — premium micro-experience",
         "Niska",
         "Cena 2 EUR pp; kombinovati sa Gardjola Gardens"],
        ["Hastings Gardens (Valletta)",
         "Nakon zalaska, marina svetla",
         "Zaklonjeno od glavne guzve, pogled na Msida Creek marinu",
         "Retka — uglavnom lokalni parovi",
         "Manje poznat od Upper Barrakka — bolji za pravu intimnost"],
        ["Xlendi / Gozo",
         "Uvece",
         "Mala bay atmosfera, vecera pored mora, setnja uz stene",
         "Niska",
         "Ukljuciti u overnight Gozo plan ili 7-day product"],
    ]
    e.append(tbl(
        ["Spot", "Najbolji termin", "Zasto romanticno", "Guzva", "Prakticna napomena"],
        rows,
        col_widths=[3.5*cm, 3*cm, 4.5*cm, 2.5*cm, 4*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 7: Zalasci ───────────────────────────────────────────────────────

def s7():
    e = [sec_hdr("7", "Zalasci sunca — Top 8"), sp(1)]
    rows = [
        ["Dingli Cliffs",
         "Auto/taksi lako; bus 201 sporije",
         "Direktan sun-over-sea, epski kadar, odlican za parove",
         "Jak vetar; hodanje blizu ivice bez ograde"],
        ["Ghajn Tuffieha / Riviera",
         "Bus do vrha + 200 stepenica",
         "Kombinacija plaze + clay slopes + mora — najlepsi beach zalazak",
         "Rip currents pri vetru; mobility issues za stepenice"],
        ["Golden Bay",
         "Odlican — bus terminus",
         "Laki pristup, dobra infrastruktura, porodice i parovi",
         "Guzva; Radisson hotel dominira pozadinom"],
        ["Dwejra Bay (Gozo)",
         "Auto ili bus iz Viktorije",
         "Dramaticne stene, Fungus Rock, tamno-zlatna svetlost",
         "Moguci jak vetar; Azure Window vise ne postoji (srusio se 2017.)"],
        ["Tal-Mixta Cave (Gozo)",
         "Auto na Gozu",
         "Prirodni okvir nad Ramla Bay — fotografski klasik",
         "Vrucina u podne, guzva, bez auta ne ide lako"],
        ["Xwejni Salt Pans (Gozo)",
         "Auto na Gozu, blizu Marsalforna",
         "Geometrijske solane + more = odlicna tekstura za fotografije",
         "Vetar/talasi na samoj ivici; nema hlada"],
        ["Upper Barrakka / Valletta blue hour",
         "Pesice iz centra Vallette",
         "Harbour blue hour — nije direktan zalazak u more, ali je odlican",
         "Gost ne sme ocekivati sunce koje pada u more — objasniti razliku"],
        ["Gardjola Gardens (Senglea)",
         "Ferry + pesice u Three Cities",
         "Harbour lights ka Valletti; bolji blue hour nego klasican sea sunset",
         "Ne ocekivati direktan sun-over-sea; kombinovati sa Dingli"],
    ]
    e.append(tbl(
        ["Spot", "Pristup", "Best za foto / parove", "Upozorenje"],
        rows,
        col_widths=[3.5*cm, 3.5*cm, 5.5*cm, 5*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 8: Hrana ─────────────────────────────────────────────────────────

def s8():
    e = [sec_hdr("8", "Lokalna hrana"), sp(1)]
    e.append(sub_hdr("Sta obavezno probati"))
    food = [
        ["Pastizzi",
         "Lisnato testo sa rikotom ili graškom. Jeftino, svuda dostupno. Apsolutni must.",
         "Svi", "High"],
        ["Stuffat tal-fenek (Fenkata)",
         "Nacionalno jelo — zeciji gulas u crvenom vinu. Meso spada sa kosti.",
         "Foodies, cultura", "High"],
        ["Ftira / hobz biz-zejt",
         "Malteska pogaca sa tunjevinom, kaparima, paradajzom, maslinama, gbejna sirom.",
         "Svi, beach piknik", "Medium"],
        ["Lampuki pie",
         "Sezonska riba lampuki u piti — vise jesen / rani jun.",
         "Foodies", "Medium"],
        ["Gbejna",
         "Lokalni sir, posebno Gozo; servira se sa paradajzom, kaparima, ftira.",
         "Foodies, Gozo", "Medium"],
        ["Bigilla",
         "Pasulj dip, obicno starter sa malteski hlebom.",
         "Parovi, porodice", "Medium"],
        ["Imqaret",
         "Przeni desert sa urmama — street food kod Vallette i na festas.",
         "Svi koji vole slatko", "Medium"],
        ["Kinnie / Cisk / lokalno vino",
         "Kinnie = gorko narandzasto pice; Cisk = lokalno pivo. Lokalna vina sve bolja.",
         "Svi", "Medium"],
    ]
    e.append(tbl(["Jelo", "Opis", "Za koga", "Conf."], food,
                 col_widths=[3.5*cm, 7*cm, 4*cm, 3*cm]))
    e.append(sp(1))

    e.append(sub_hdr("Gde jesti — zone"))
    zones = [
        ["Valletta",
         "Premium i fine dining. Merchant St, St Lucia St. Birati manje konobe u sporednim ulicama."],
        ["Marsaxlokk",
         "Riba i morski plodovi uz luku. NE ici u nedelju (guzva/bazar). Ici sredom ili cetvrtkom uvece."],
        ["Mgarr / Rabat",
         "Tradicionalna kuhinja — zeciji gulas. Nize cene, ogromne porcije."],
        ["Gozo (Victoria / Xlendi / Marsalforn)",
         "Ftira, gbejna, morski plodovi. Lokalniji osecaj nego na Malti."],
        ["Sliema / St Julian's",
         "Prakticna turisticka zona. Veliki izbor, prosecni kvalitet."],
    ]
    e.append(tbl(["Zona", "Komentar"], zones, col_widths=[5*cm, 12.5*cm]))
    e.append(sp(1))
    e.append(warn_box(
        "IZBEGAVATI: Restorani sa agresivnim hosesima, 'Tourist menu' za 15 EUR "
        "(odmrznuti uvozni file), riba bez jasno navedene cene po kilogramu, genericki "
        "italijanski meniji bez malteskig jela. "
        "Sveza lokalna riba uvek se naplacuje po kilogramu — ocekivati 25-30 EUR+ po osobi."
    ))
    e.append(PageBreak())
    return e

# ── Sekcija 9: Sta izbegavati ─────────────────────────────────────────────────

def s9():
    e = [sec_hdr("9", "Sta izbegavati — Top 15 upozorenja"), sp(1)]
    warns = [
        ["W1",  "NE prodavati Maltu kao Maldives-style beach",
         "Vise od 50% obale je kamenita. Klijent ce biti razocaran. Uvek postavi ocekivanja."],
        ["W2",  "NE slati porodice u Paceville",
         "Nightlife zona — buka do zore, pijanci. Smestaj samo za party travelers."],
        ["W3",  "NE preporucivati Blue Lagoon u podne jul/avg",
         "Katastrofalna guzva, brodovi ispustaju gasove, nema hlada, nema prostora. QR booking sistem je obavezan od 2025/2026."],
        ["W4",  "NE oslanjati se samo na bus za hidden beaches",
         "Za Fomm ir-Rih, St Peter's Pool, Gnejna, Ghar Lapsi — bus je redak ili ne postoji. Auto/taksi neophodni."],
        ["W5",  "NE pretrpavati 3-day itinerary",
         "Malta izgleda mala, ali bus + saobracaj + vrucina usporavaju sve. Max 3 stavke po danu."],
        ["W6",  "NE rezervisati hotel samo po 'distance to beach'",
         "300m do mora moze znaciti stene i beton, ne pesak. Uvek proveriti Google Maps satelit."],
        ["W7",  "NE preskakati proveru svezih recenzija",
         "Proveriti poslednjih 30-90 dana na Booking.com i TripAdvisor. Keywords: construction, drilling, crane, noise, AC."],
        ["W8",  "Paziti na construction buku",
         "Malta je permanentno gradiliste. Hotel sa odlicnom prosecnom ocenom moze imati kran pored prozora."],
        ["W9",  "Paziti na AC u letnjoj sezoni",
         "Stare kamene zgrade akumuliraju toplotu. Bez funkcionalne klime leti = neizdrzivo. Uvek proveriti recenzije."],
        ["W10", "Paziti na 'real beach' vs 'rocky coast'",
         "Sliema, Gzira, Valletta, Three Cities = kamen i beton. Pesak uglavnom na severu i severozapadu."],
        ["W11", "Paziti na vetar, talase i crvene zastavice",
         "Golden Bay i Ghajn Tuffieha su osetljive na Majjistral (NW vetar) — struje postaju opasne."],
        ["W12", "NE ici u Marsaxlokk u nedelju ako gost mrzi guzve",
         "Nedeljni fish market je zapravo turisticki bazar. Preporuciti sredu/cetvrtak."],
        ["W13", "NE tretirati Gozo kao '2 sata usput'",
         "Gozo zasluzuje ceo dan. Dwejra, Ramla, Victoria, salt pans, Wied il-Ghasri = pun dan."],
        ["W14", "NE preporucivati cliff/pool spotove neplivacima",
         "St Peter's Pool, Ghar Lapsi, Wied il-Ghasri — nema lifeguarda, ulaz/izlaz samo skakanjem/merdevinama."],
        ["W15", "Hal Saflieni Hypogeum bez rane rezervacije",
         "Ulaznice se rasprodaju 3-4 meseca unapred. Last-minute ne radi."],
    ]
    e.append(tbl(["#", "Upozorenje", "Detalj"], warns,
                 col_widths=[1*cm, 6*cm, 10.5*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 10: 3-Day ─────────────────────────────────────────────────────────

def s10():
    e = [sec_hdr("10", "3-Day Itinerary (realan, nije pretrpan)"), sp(1)]
    e.append(info_box("Tempo: max 3 stavke po danu. Uvece — setnja umesto dodavanja novih lokacija."))
    e.append(sp(1))

    e.append(sub_hdr("Day 1: Valletta + Three Cities"))
    e.append(tbl(["Deo dana", "Plan"], [
        ["Jutro",
         "Valletta: City Gate, Republic Street, St John's Co-Cathedral (bukirati unapred). "
         "Upper Barrakka u 11:45 za gun salute u 12:00."],
        ["Podne / popodne",
         "Barrakka Lift do pristanica. Tradicional. camac (dghajsa, 2 EUR pp) do Birgu/Vittoriosa. "
         "Setnja marina, Fort St Angelo pogled, Gardjola Gardens u Senglei."],
        ["Uvece",
         "Povratak ferryjem u Vallettu. Vecera u sporednim ulicama blizu pijace. "
         "Nocna setnja uz osvetljene zidine."],
        ["Rizici",
         "Letnja podnevna vrucina: Three Cities preporuciti za 15:00+. "
         "Hotel daleko na severu = kasni povratak bus problem."],
    ], col_widths=[3*cm, 14.5*cm]))
    e.append(sp(1))

    e.append(sub_hdr("Day 2: Mdina / Rabat + Plaze + Zalazak"))
    e.append(tbl(["Deo dana", "Plan"], [
        ["Jutro",
         "Mdina rano (pre turistickih grupa). Kafa u Fontanella baru sa pogledom na centralnu Maltu."],
        ["Podne / popodne",
         "Rucak u Rabatu (pastizzi u Crystal Palace ili tradicionalna konoba). "
         "Odlazak na Golden Bay (laksi pristup, porodice) ili Ghajn Tuffieha (lepsa, stepenice)."],
        ["Uvece",
         "Zalazak: Dingli Cliffs (auto/taksi preporuceno). Vecera u Rabatu — zeciji gulas."],
        ["Rizici",
         "Jak NW vetar = birati Golden Bay umesto Ghajn Tuffieha. "
         "Stepenice na Ghajn Tuffieha = mobility problem za starije i decu."],
    ], col_widths=[3*cm, 14.5*cm]))
    e.append(sp(1))

    e.append(sub_hdr("Day 3: Marsaxlokk + Jug Malte + Uvece Sliema / Spinola"))
    e.append(tbl(["Deo dana", "Plan"], [
        ["Jutro",
         "Marsaxlokk: ribarska luka, setnja pored sarenih luzzu camaca. "
         "NE ici u nedelju ako gost mrzi guzve (bazar umesto autenticnosti)."],
        ["Podne / popodne",
         "St Peter's Pool (za plivace/avanturiste) ILI Blue Grotto viewpoint (za sve, "
         "brodicem ako more dozvoljava). Rucak u lokalu blizu."],
        ["Uvece",
         "Povratak u Sliemu ili St Julian's. Setnja promenadoim ili Spinola Bay. "
         "Zavrsna vecera uz vodu."],
        ["Rizici",
         "St Peter's Pool: samo za dobre plivace. Auto/taksi neophodan. "
         "Ako ostajete u Melliehi — adaptirati uvece na Mellieha village."],
    ], col_widths=[3*cm, 14.5*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 11: 5-Day ─────────────────────────────────────────────────────────

def s11():
    e = [sec_hdr("11", "5-Day Itinerary"), sp(1)]
    e.append(info_box("Graditi na 3-day planu. Dodati: Comino rano ujutru, Gozo ceo dan, juzna Malta + food dan."))
    e.append(sp(1))
    days = [
        ["Day 1", "Valletta + Three Cities",
         "Kao Day 1 u 3-day planu. Luksuznije opcije vecere."],
        ["Day 2", "Mdina / Rabat + Dingli zalazak",
         "Kultura + zalazak. Vecera sa zecijem gulasem u Rabatu."],
        ["Day 3", "Plaze — sever / severozapad",
         "Golden Bay ili Ghajn Tuffieha. Zalazak ako uslovi dobri."],
        ["Day 4", "Gozo — ceo dan",
         "Trajekt iz Cirkewwe. Victoria/Cittadella, Ramla Bay, Tal-Mixta Cave, "
         "sol pans ili Dwejra. Zalazak na Gozu. Kasni trajekt nazad."],
        ["Day 5", "Juzna Malta + lokalna hrana",
         "Marsaxlokk (ne u nedelju), St Peter's Pool ili Blue Grotto, "
         "opciono Hagar Qim/Mnajdra hramovi. Vecera na moru."],
    ]
    e.append(tbl(["Dan", "Fokus", "Detalji"], days,
                 col_widths=[1.5*cm, 4*cm, 12*cm]))
    e.append(sp(1))
    e.append(Paragraph(
        "Rizici: Gozo zahteva rani start. Blue Lagoon nije u ovom 5-day planu — "
        "ako gost insistira, ubaciti rano jutro Day 4 (08:00) pre Gozo ture.",
        sNote))
    e.append(PageBreak())
    return e

# ── Sekcija 12: 7-Day ─────────────────────────────────────────────────────────

def s12():
    e = [sec_hdr("12", "7-Day Itinerary (Malta + Gozo + Comino)"), sp(1)]
    days = [
        ["Day 1", "Valletta — sporiji dolazak",
         "Upper Barrakka, stare ulice, vecera u harbour zoni. Bez pretrpavanja."],
        ["Day 2", "Three Cities + Sliema ferry",
         "Birgu/Senglea ujutru/popodne. Ferry Valletta-Sliema za blue hour. Nocna setnja."],
        ["Day 3", "Mdina / Rabat + Dingli",
         "Silent City, lokalna hrana u Rabatu, Dingli Cliffs zalazak."],
        ["Day 4", "Severne plaze",
         "Mellieha Bay (porodice) ili Golden/Ghajn Tuffieha (parovi). Alternativni bay pri losem vetru."],
        ["Day 5", "Comino — Blue Lagoon",
         "ICI RANO (08:00, prvi brodic). QR booking / shore access obavezan. Napustiti do 11:30. "
         "Popodne odmor ili Paradise Bay."],
        ["Day 6", "Gozo — pun dan",
         "Dwejra, Inland Sea, Victoria/Cittadella, Ramla Bay/Tal-Mixta, sol pans. Zalazak na Gozu."],
        ["Day 7", "Juzna Malta + fleksibilan kraj",
         "Marsaxlokk, St Peter's Pool/Blue Grotto, ili Hypogeum ako bukiran. Vecernji shopping/setnja."],
    ]
    e.append(tbl(["Dan", "Fokus", "Detalji"], days,
                 col_widths=[1.5*cm, 4*cm, 12*cm]))
    e.append(sp(1))
    e.append(sub_hdr("Alternativa za kisu / jak vetar / guzve"))
    e += bul([
        "Valletta muzeji: National Museum of Archaeology, Lascaris War Rooms, St John's Co-Cathedral.",
        "San Anton Gardens (besplatno, pogodno za sve).",
        "Malta National Aquarium (Qawra) — odlicno za porodice.",
        "Esplora Interactive Science Centre (Kalkara) — porodice sa decom.",
        "Mdina / Rabat unutrasnjost — crkve, konobe, setnja.",
        "Ako su zapadne plaze blokirane vetrom: preci na bays prema istoku/jugu.",
    ])
    e.append(PageBreak())
    return e

# ── Sekcija 13: Hotel Booking Logic ──────────────────────────────────────────

def s13():
    e = [sec_hdr("13", "Hotel Booking Logic"), sp(1)]
    rows = [
        ["Porodice",
         "Mellieha, St Paul's Bay / Qawra",
         "Deciji bazen, lift, realna udaljenost do pescane plaze, velicina sobe",
         "Paceville, strme ulice Vallette, tiny boutique rooms"],
        ["Beach stay",
         "Mellieha Bay, Golden Bay resort zona, Paradise Bay / Marfa",
         "Da li je privatna plaza ili rocky coast; da li su lezaljke ukljucene",
         "Valletta, Gzira, Sliema ako gost trazi pesak"],
        ["Budget",
         "Gzira, Bugibba / Qawra, delovi Slieme",
         "Funkcionalna klima, pritisak vode, blizina bus terminusa",
         "Medeni mesec, luxury ocekivanja"],
        ["Nightlife",
         "St Julian's / Paceville",
         "Zvucna izolacija (double-glazing), bezbednost u/oko hotela nocu",
         "Porodice, seniors, romanticni odmor"],
        ["Parovi / romanticno",
         "Valletta boutique, Three Cities boutique, Mdina, Gozo farmhouse / Xlendi",
         "Krovni pogled, soba sa prozorom (ne atrijum), recenzije atmosfere",
         "Ako gost zeli resort beach only"],
        ["Luxury",
         "Valletta luxury boutique, St Julian's 5*, Gozo Kempinski",
         "Da li lido/bazen prodaje dnevne karte posjetiocima — guzva problem",
         "Budget ocekivanja"],
    ]
    e.append(tbl(
        ["Segment", "Najbolja zona", "Sta proveriti", "Izbegavati"],
        rows,
        col_widths=[3.5*cm, 4*cm, 6*cm, 4*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 14: Hotel QA Checklist ───────────────────────────────────────────

def s14():
    e = [sec_hdr("14", "Manual Hotel QA Checklist"), sp(1)]
    e.append(Paragraph("Pre nego agent preporuci hotel — proci kroz svaku tacku:", sH3))
    e.append(sp(1))
    items = [
        ["1",  "Svezerecenzije (30-90 dana)",
         "Filtrirati na Booking.com i TripAdvisor — samo najnovije. Prosecna ocena je lazna ako je stara."],
        ["2",  "Construction / buka",
         "Keywords u recenzijama: construction, drilling, crane, building site, noise, jackhammer."],
        ["3",  "Status renoviranja",
         "'Recently renovated' proveriti po sobama — ne samo lobby fotografije."],
        ["4",  "Bazen otvoren / kapacitet",
         "Proveriti: da li je otvoren u konkretnom mesecu; da li se prodaju dnevne karte vanjskim gostima."],
        ["5",  "Realna udaljenost od plaze",
         "Google Maps satelit: da li vodi do pescane plaze ili kamenite obale/promenade."],
        ["6",  "AC u sezoni",
         "Leti je klima non-negotiable. Proveriti recenzije za: no AC, broken AC, hot room."],
        ["7",  "Lift / pristupacnost",
         "Valletta / Three Cities / Mdina — stare zgrade bez lifta ceste. Obavezno proveriti."],
        ["8",  "Tacna ulica i buka",
         "St Julian's: razlika izmedju Spinola Bay (tiho) i 50m dalje u Paceville (kaos)."],
        ["9",  "Gost fotografije vs hotel fotografije",
         "Sirokokulni objektiv cini bazen od 4m olimpijskim. Guest photos = realnost."],
        ["10", "Prevoz i pristup",
         "Blizina bus linije, kasni nocni povratak, parking ako gost ima auto."],
        ["11", "Politika otkazivanja",
         "Peak sezona = skupa karta — preporuciti free cancellation ili flexible rate."],
    ]
    e.append(tbl(["#", "Stavka", "Detalj"], items,
                 col_widths=[0.8*cm, 4.2*cm, 12.5*cm]))
    e.append(PageBreak())
    return e

# ── Sekcija 15: Product Ideas ─────────────────────────────────────────────────

def s15():
    e = [sec_hdr("15", "Product Ideas za D&L Project56"), sp(1)]
    rows = [
        ["Malta 3-Day Quick Plan",
         "First-timers, kratki odmor",
         "Ne znaju odakle krenuti, boje se da nece stici nista",
         "7-12 EUR *",
         "Upgrade na 5-day plan"],
        ["Malta 5-Day Perfect Plan",
         "Parovi, porodice",
         "Zele balans plaze + kultura + Gozo — logistika nejasna",
         "12-18 EUR *",
         "Romantic ili Family add-on"],
        ["Malta Romantic Plan",
         "Parovi, godisnjice",
         "Gde su pravi romanticni spotovi, zalasci, vecere",
         "12-15 EUR *",
         "Hotel area guide"],
        ["Malta Family Beach Plan",
         "Porodice sa malom decom",
         "Koje plaze su bezbedne, gde smestiti porodicu",
         "10-15 EUR *",
         "Hotel booking guide"],
        ["Malta Where to Stay Guide",
         "Svi segmenti, pre-booking",
         "Koja zona odgovara kakvom gostu",
         "8-12 EUR *",
         "Standalone ili bundle"],
        ["Malta Gozo + Comino Plan",
         "Island hopping fokus",
         "Logistika trajekta, Blue Lagoon timing, Gozo highlights",
         "10-15 EUR *",
         "7-day plan bundle"],
        ["Malta No-Car Itinerary",
         "Turisti bez auta",
         "Sta moze bez rent-a-cara, koje plaze dostupne busom",
         "8-12 EUR *",
         "3 ili 5-day plan"],
        ["Malta Hotel Area Mistakes Guide",
         "Pre-booking faza",
         "Kako ne rezervisati hotel u pogresnoj zoni",
         "6-9 EUR *",
         "Where to Stay Guide"],
    ]
    e.append(tbl(
        ["PDF Proizvod", "Target kupac", "Pain point", "Price idea", "Upsell"],
        rows,
        col_widths=[4.5*cm, 3*cm, 4.5*cm, 2*cm, 3.5*cm]))
    e.append(sp(1))
    e.append(Paragraph(
        "* Sve price ideas su orijentacione — nisu verifikovane trizisno. "
        "Oznacene su kao 'price idea', nisu finalne cene.",
        sNote))
    e.append(PageBreak())
    return e

# ── Sekcija 16: Lejla Approval ────────────────────────────────────────────────

def s16():
    e = []
    hdr = Table([[Paragraph("16.  LEJLA — REVIEW &amp; APPROVAL", sH1)]], colWidths=[17.5*cm])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), ORANGE),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
    ]))
    e.append(hdr)
    e.append(sp(2))
    e.append(Paragraph(
        "Ovaj dokument je spreman za tvoj pregled. Procitaj, oznaci odgovore i vrati feedback. "
        "Nijedan PDF proizvod ne ide u produkciju dok ne dobijem tvoje odobrenje.",
        sApprove))
    e.append(sp(2))
    e.append(HRFlowable(width="100%", thickness=1, color=ORANGE))
    e.append(sp(1))

    questions = [
        {"num": "1", "q": "Da li je Malta dobar prvi paid PDF travel product?",
         "opts": ["Da — krecemo", "Da, ali treba jos istrazivanja", "Ne — birati drugu destinaciju"]},
        {"num": "2", "q": "Koji segment gadamo PRVI?",
         "opts": ["Parovi", "Porodice", "First-time Malta (general)", "No-car travelers"]},
        {"num": "3", "q": "Da li idemo sa 3/5/7-day PDF paketima?",
         "opts": ["Da — sva tri", "Samo 3 i 5-day", "Kreni sa jednim (naznaci kojim)", "Drugacija struktura"]},
        {"num": "4", "q": "Da li prvo pravimo jedan premium PDF ili vise manjih?",
         "opts": ["Jedan sveobuhvatni premium PDF", "Vise manjih po segmentu", "Bundle paket (3 u 1)"]},
        {"num": "5", "q": "Da li se slazas da Blue Lagoon i hotel-zone warnings budu jako naglaseni?",
         "opts": ["Da — jako naglasiti", "Umereno — ne plasiti klijente", "Preformulisati neutralno"]},
        {"num": "6", "q": "Finalna ocena dokumenta",
         "opts": ["APPROVED — krecemo u produkciju",
                  "NEEDS CHANGES — detalji u napomenama ispod",
                  "REJECT — objasni razlog"]},
    ]

    for q in questions:
        qh = Table([[Paragraph(
            f"Pitanje {q['num']}: {q['q']}",
            S("qh", fontSize=10, fontName="Helvetica-Bold",
              textColor=DARK_NAVY, leading=14)
        )]], colWidths=[17.5*cm])
        qh.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), LIGHT_BLUE),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("LINEBELOW",     (0,0), (-1,-1), 1, MID_BLUE),
        ]))
        e.append(qh)
        for opt in q["opts"]:
            ot = Table([[
                Paragraph("[ ]", S("cb", fontSize=10, fontName="Helvetica",
                                   textColor=MID_BLUE, leading=13)),
                Paragraph(opt, sApprove)
            ]], colWidths=[0.8*cm, 16.7*cm])
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

    notes = Table([
        [Paragraph("Napomene / Komentari Lejle:", S("nl", fontSize=10,
             fontName="Helvetica-Bold", textColor=DARK_NAVY, leading=13))],
        [Paragraph("\n\n\n\n\n\n\n\n", sBody)],
    ], colWidths=[17.5*cm])
    notes.setStyle(TableStyle([
        ("BOX",           (0,0), (-1,-1), 1, MID_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("BACKGROUND",    (0,0), (0,0), LIGHT_BLUE),
        ("LINEBELOW",     (0,0), (0,0), 0.5, MID_BLUE),
    ]))
    e.append(notes)
    e.append(sp(2))

    footer = Table([[Paragraph(
        "D&amp;L Project56 — Malta Travel Product Pool  |  Internal Review v1.1  |  26.06.2026.  |  "
        "INTERNO — Nije za distribuciju klijentima",
        S("f", fontSize=7, textColor=colors.HexColor("#888888"),
          fontName="Helvetica", alignment=TA_CENTER, leading=10)
    )]], colWidths=[17.5*cm])
    footer.setStyle(TableStyle([
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("LINEABOVE",  (0,0), (-1,-1), 0.5, MED_GREY),
    ]))
    e.append(footer)
    return e

# ── Page footer ───────────────────────────────────────────────────────────────

def on_page(canvas, doc):
    canvas.saveState()
    pg = canvas.getPageNumber()
    if pg > 1:
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#888888"))
        canvas.drawRightString(
            A4[0] - 1.5*cm, 0.8*cm,
            f"D&L Project56 — Malta Internal Review v1.1  |  Strana {pg}"
        )
        canvas.setStrokeColor(MED_GREY)
        canvas.setLineWidth(0.3)
        canvas.line(1.5*cm, 1.2*cm, A4[0] - 1.5*cm, 1.2*cm)
    canvas.restoreState()

# ── Build ─────────────────────────────────────────────────────────────────────

def build():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=1.5*cm,  bottomMargin=1.8*cm,
        title="D&L Project56 — Malta Travel Product Internal Review v1.1",
        author="D&L Project56 AI Engine",
        subject="Internal Product Review for Lejla",
    )
    story = []
    story += cover()
    story += toc()
    story += s1()
    story += s2()
    story += s3()
    story += s4()
    story += s5()
    story += s6()
    story += s7()
    story += s8()
    story += s9()
    story += s10()
    story += s11()
    story += s12()
    story += s13()
    story += s14()
    story += s15()
    story += s16()
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF v1.1 generated: {OUTPUT_PATH}")

if __name__ == "__main__":
    build()
