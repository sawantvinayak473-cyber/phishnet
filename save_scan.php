<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");
include "db.php";

// Read JSON body
$data = json_decode(file_get_contents("php://input"), true);

$input_text = $data["input_text"] ?? "";
$result = $data["result"] ?? "";
$risk_score = $data["risk_score"] ?? 0;
$scan_type = $data["scan_type"] ?? "";

$sql = "INSERT INTO scans (input_text, result, risk_score, scan_type)
        VALUES (?, ?, ?, ?)";

$stmt = $conn->prepare($sql);
$stmt->bind_param("ssis", $input_text, $result, $risk_score, $scan_type);
$stmt->execute();

echo "saved";
?>