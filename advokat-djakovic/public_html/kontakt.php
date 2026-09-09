<?php
/* Контакт форма — Адвокат Бојана Ђаковић
   Мења се само у секцији ПОДЕШАВАЊА испод. */

/* ---------- ПОДЕШАВАЊА ---------- */
$PRIMALAC   = 'advokat.bdjakovic@gmail.com';
$SITE       = 'https://bojanadjakovic.rs';
$POSILJALAC = 'no-reply@bojanadjakovic.rs';
$POVRATAK   = $SITE . '/?sent=1#kontakt';
$GRESKA     = $SITE . '/?sent=0#kontakt';
$RAZMAK_SEK = 60; /* rate-limit: једно слање у 60 секунди по сесији */
/* -------------------------------- */

session_start();

function odlazi($url) { header('Location: ' . $url, true, 303); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { odlazi($SITE . '/#kontakt'); }

/* honeypot */
if (!empty($_POST['website'])) { odlazi($POVRATAK); }

/* rate-limit по сесији */
$sada = time();
if (isset($_SESSION['zadnje_slanje']) && ($sada - (int)$_SESSION['zadnje_slanje']) < $RAZMAK_SEK) {
    odlazi($GRESKA);
}

$ime     = trim((string)($_POST['ime'] ?? ''));
$telefon = trim((string)($_POST['telefon'] ?? ''));
$mejl    = trim((string)($_POST['email'] ?? ''));
$poruka  = trim((string)($_POST['poruka'] ?? ''));
$sagl    = isset($_POST['saglasnost']) && $_POST['saglasnost'] === '1';

/* валидација */
if ($ime === '' || mb_strlen($ime) > 80)         { odlazi($GRESKA); }
if ($poruka === '' || mb_strlen($poruka) > 3000) { odlazi($GRESKA); }
if (!$sagl)                                      { odlazi($GRESKA); }

/* бар један податак за контакт: телефон ИЛИ мејл */
if ($telefon === '' && $mejl === '') { odlazi($GRESKA); }

if ($telefon !== '') {
    if (mb_strlen($telefon) > 40)                            { odlazi($GRESKA); }
    if (!preg_match('/^[0-9 +\/().\-]{6,40}$/u', $telefon))   { odlazi($GRESKA); }
}
if ($mejl !== '') {
    if (mb_strlen($mejl) > 120)                        { odlazi($GRESKA); }
    if (!filter_var($mejl, FILTER_VALIDATE_EMAIL))     { odlazi($GRESKA); }
}

/* заштита од убацивања заглавља */
$ime     = str_replace(array("\r", "\n"), ' ', $ime);
$telefon = str_replace(array("\r", "\n"), ' ', $telefon);
$mejl    = str_replace(array("\r", "\n"), ' ', $mejl);

$naslov = '=?UTF-8?B?' . base64_encode('Питање са сајта — ' . $ime) . '?=';

$telo  = "Питање преко сајта bojanadjakovic.rs\n";
$telo .= "-----------------------------------\n";
$telo .= "Име и презиме: $ime\n";
$telo .= "Телефон: " . ($telefon !== '' ? $telefon : '-') . "\n";
$telo .= "Мејл: "    . ($mejl    !== '' ? $mejl    : '-') . "\n";
$telo .= "Време: " . date('d.m.Y. H:i') . "\n";
$telo .= "IP: " . ($_SERVER['REMOTE_ADDR'] ?? '-') . "\n";
$telo .= "Сагласност за контакт: да\n";
$telo .= "-----------------------------------\n\n";
$telo .= $poruka . "\n";

/* Reply-To иде на мејл пошиљаоца ако га је оставио, иначе на канцеларију */
$odgovor_na = ($mejl !== '') ? $mejl : $PRIMALAC;

$zaglavlja  = "MIME-Version: 1.0\r\n";
$zaglavlja .= "Content-Type: text/plain; charset=UTF-8\r\n";
$zaglavlja .= "Content-Transfer-Encoding: 8bit\r\n";
$zaglavlja .= "From: Sajt <" . $POSILJALAC . ">\r\n";
$zaglavlja .= "Reply-To: " . $odgovor_na . "\r\n";

$poslato = @mail($PRIMALAC, $naslov, $telo, $zaglavlja);

$_SESSION['zadnje_slanje'] = $sada;

odlazi($poslato ? $POVRATAK : $GRESKA);
