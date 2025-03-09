<?php
// Enable error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Database configuration
$host = 'localhost'; // Change if not running locally
$dbname = 'Kazi';    // Ensure the database exists
$username = 'phelix';  // Ensure this user exists and has access
$password = 'phelix'; // Ensure this password is correct

try {
    // Create a new PDO instance
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    
    // Set the PDO error mode to exception
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    echo "Connected successfully to the database.";
} catch (PDOException $e) {
    // Output the specific error message
    echo "Connection failed: " . $e->getMessage();
}
?>