<?php
$conn = new mysqli("localhost", "root", "", "phishnet_db");
if ($conn->connect_error) {
    die("DB connection failed: " . $conn->connect_error);
}
?>