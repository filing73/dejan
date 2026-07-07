<?php
declare(strict_types=1);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$maxBytes = 256 * 1024;
$body = file_get_contents('php://input', false, null, 0, $maxBytes + 1);

if ($body === false) {
    http_response_code(400);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Unable to read request body']);
    exit;
}

if (strlen($body) > $maxBytes) {
    http_response_code(413);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Request body too large']);
    exit;
}

$backendUrl = 'http://127.0.0.1:3100/api/chat';

$ch = curl_init($backendUrl);
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $body,
    CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 15,
    CURLOPT_CONNECTTIMEOUT => 5,
]);

$response = curl_exec($ch);
$statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$contentType = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
curl_close($ch);

if ($response === false) {
    http_response_code(502);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Backend unavailable']);
    exit;
}

http_response_code($statusCode ?: 502);
header('Content-Type: ' . ($contentType ?: 'application/json'));
echo $response;
