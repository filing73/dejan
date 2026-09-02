<?php
/* Контакт форма — Адвокат Бојана Ђаковић
   Мења се само у секцији ПОДЕШАВАЊА испод. */

/* ---------- ПОДЕШАВАЊА ---------- */
$PRIMALAC   = 'advokat.bdjakovic@gmail.com';
$SITE       = 'https://advokatdjakovic.rs';
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
$poruka  = trim((string)($_POST['poruka'] ?? ''));
$sagl    = isset($_POST['saglasnost']) && $_POST['saglasnost'] === '1';

/* валидација */
if ($ime === '' || mb_strlen($ime) > 80)          { odlazi($GRESKA); }
if ($telefon === '' || mb_strlen($telefon) > 40)  { odlazi($GRESKA); }
if (!preg_match('/^[0-9 +\/().\-]{6,40}$/u', $telefon)) { odlazi($GRESKA); }
if ($poruka === '' || mb_strlen($poruka) > 3000)  { odlazi($GRESKA); }
if (!$sagl)                                       { odlazi($GRESKA); }

/* заштита од убацивања заглавља */
$ime     = str_replace(array("\r", "\n"), ' ', $ime);
$telefon = str_replace(array("\r", "\n"), ' ', $telefon);

$naslov = '=?UTF-8?B?' . base64_encode('Упит са сајта — ' . $ime) . '?=';

$telo  = "Упит преко сајта advokatdjakovic.rs\n";
$telo .= "-----------------------------------\n";
$telo .= "Име и презиме: $ime\n";
$telo .= "Телефон: $telefon\n";
$telo .= "Време: " . date('d.m.Y. H:i') . "\n";
$telo .= "IP: " . ($_SERVER['REMOTE_ADDR'] ?? '-') . "\n";
$telo .= "Сагласност за контакт: да\n";
$telo .= "-----------------------------------\n\n";
$telo .= $poruka . "\n";

$zaglavlja  = "MIME-Version: 1.0\r\n";
$zaglavlja .= "Content-Type: text/plain; charset=UTF-8\r\n";
$zaglavlja .= "Content-Transfer-Encoding: 8bit\r\n";
$zaglavlja .= "From: Sajt <no-reply@advokatdjakovic.rs>\r\n";
$zaglavlja .= "Reply-To: " . $PRIMALAC . "\r\n";

$poslato = @mail($PRIMALAC, $naslov, $telo, $zaglavlja);

$_SESSION['zadnje_slanje'] = $sada;

odlazi($poslato ? $POVRATAK : $GRESKA);
