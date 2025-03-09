<?php
header('Content-Type: application/json');

// Database connection
$host = 'localhost';
$db = 'Kazi';
$user = 'phelix';
$pass = 'phelix';

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die(json_encode(['success' => false, 'message' => 'Database connection failed']));
}

// Get input data
$data = json_decode(file_get_contents('php://input'), true);
$email = $data['email'];
$password = $data['password'];

// Fetch employer data
$stmt = $conn->prepare('SELECT * FROM users WHERE email = ? AND role = "employer"');
$stmt->bind_param('s', $email);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 0) {
    echo json_encode(['success' => false, 'message' => 'User not found']);
    exit;
}

$user = $result->fetch_assoc();

// Verify password
if (password_verify($password, $user['password_hash'])) {
    echo json_encode(['success' => true, 'message' => 'Login successful']);
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid password']);
}

$stmt->close();
$conn->close();
?>