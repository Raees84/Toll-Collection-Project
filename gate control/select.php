<?php

$servername = "104.155.170.169";
$dBUsername = "root";
$dBPassword = "G00dwill";
$dBName = "tollcollection";

$conn = mysqli_connect($servername, $dBUsername, $dBPassword, $dBName);

if (!$conn) {
	die("Connection failed: ".mysqli_connect_error());

	echo "Connection to database failed.";
}

$tollFee = 2;
$uidString = $_POST['selectVehicle'];
//echo "post string";
//echo $uidString;

$transactions = 6;

if(isset($_POST['selectVehicle']))
{
	$uidString = $_POST['selectVehicle'];
	//echo "post string";
	//echo $uidString;
	
	
	$sql = "SELECT username FROM vehicles WHERE registrationNumber = '$uidString';";
	$result   = mysqli_query($conn, $sql);
	$row  = mysqli_fetch_assoc($result);

	if ($row['username'] == NULL)
	{
		echo "Vehicle not registered.";
	}

	else
	{
		$motorist = $row['username'];
		$sql = "SELECT balance FROM balances WHERE username = '$motorist';";
		$result   = mysqli_query($conn, $sql);
		$row  = mysqli_fetch_assoc($result);
		$balance = $row['balance'];
	
		if($balance < $tollFee)
		{
			echo "Insufficient funds.";
		}

		else
		{
			$sql = "UPDATE balances SET balance = balance - '$tollFee' WHERE username = '$motorist';";
			$update   = mysqli_query($conn, $sql);
			
			date_default_timezone_set("Africa/Mbabane");
			$date = date('m/d/Y h:i:s a', time());
			
			$historySQL = "INSERT INTO  tollhistory (timestamp, registrationNumber, gateName, username) VALUES ('$date', '$uidString', 'Matsapha', '$motorist')";  
			$insert = mysqli_query($conn, $historySQL);
			
			$transactions = $transactions + 1;
			
			$transactionHistorySQL = "INSERT INTO  transactionhistory (transactionID, description, username, amount, timestamp) VALUES ('$transactions', 'Payment', '$motorist', '$tollFee', '$date')";  
			$insertTransaction = mysqli_query($conn, $transactionHistorySQL);
		
			echo "Transaction successful.";
		}
		
	}
}
else
    echo "uidString is empty";


?>


