<?php
/**
 * D&L AI Sales Assistant - server-side proxy.
 *
 * The browser talks ONLY to this file (/ai-proxy.php). This file forwards the
 * request to the local AI backend that runs on the same server:
 *
 *     http://127.0.0.1:3100/api/chat
 *
 * The DeepSeek (or any other) API key lives ONLY on the backend service, never
 * here and never in the browser. This keeps the key off the public internet.
 *
 * NOTE: This proxy only works once uploaded to the Hestia subdomain where the
 * backend service (port 3100) is reachable. Locally it will fail to connect,
 * which is expected — the widget UI is built to degrade gracefully.
 */

declare(strict_types=1);

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------
const BACKEND_URL  = 'http://127.0.0.1:3100/api/chat';
const TIMEOUT_SECS = 30;
const MAX_BODY     = 64 * 1024; // 64 KB cap on incoming payloads

// ---------------------------------------------------------------------------
// Headers / CORS (same-origin expected, but be explicit)
// ---------------------------------------------------------------------------
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

/** Emit a JSON error and stop. */
function fail(int $status, string $message): void {
    http_response_code($status);
    echo json_encode([
        'error' => true,
        'reply' => $message,
    ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

// ---------------------------------------------------------------------------
// Method guard
// ---------------------------------------------------------------------------
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'POST') {
    fail(405, 'Method not allowed. Use POST.');
}

// ---------------------------------------------------------------------------
// Read + validate the incoming body
// ---------------------------------------------------------------------------
$raw = file_get_contents('php://input', false, null, 0, MAX_BODY + 1);
if ($raw === false || $raw === '') {
    fail(400, 'Empty request body.');
}
if (strlen($raw) > MAX_BODY) {
    fail(413, 'Request too large.');
}

$payload = json_decode($raw, true);
if (!is_array($payload)) {
    fail(400, 'Invalid JSON.');
}

// Whitelist the fields we forward. Nothing else is passed through.
$forward = [
    'message'      => isset($payload['message']) ? (string) $payload['message'] : '',
    'page_url'     => isset($payload['page_url']) ? (string) $payload['page_url'] : '',
    'page_title'   => isset($payload['page_title']) ? (string) $payload['page_title'] : '',
    'page_context' => isset($payload['page_context']) ? (string) $payload['page_context'] : '',
    'history'      => isset($payload['history']) && is_array($payload['history']) ? $payload['history'] : [],
];

if (trim($forward['message']) === '') {
    fail(400, 'Missing "message".');
}

$body = json_encode($forward, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

// ---------------------------------------------------------------------------
// Forward to the local backend
// ---------------------------------------------------------------------------
$ch = curl_init(BACKEND_URL);
curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => $body,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => TIMEOUT_SECS,
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_HTTPHEADER     => [
        'Content-Type: application/json',
        'Accept: application/json',
    ],
]);

$response = curl_exec($ch);
$httpCode = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlErr  = curl_error($ch);
curl_close($ch);

if ($response === false) {
    // Backend unreachable (e.g. not uploaded yet, or service down).
    fail(502, 'AI backend is not reachable right now. Please try again shortly.');
}

// Pass the backend status + payload straight through to the browser.
if ($httpCode >= 400) {
    http_response_code($httpCode);
}

echo $response;
