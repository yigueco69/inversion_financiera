<?php     
    // Fill these in with the information from your CoinPayments.net account. 
    resource pg_connect ( "host=localhost port=5432 dbname=Desarrollo user=openpg password=openpgpwd" )


    $cp_merchant_id = '2c7b76970e7e4a26e9957f4b277c5ace'; 
    $cp_ipn_secret = 'porra69mejores132porra@69'; 
    $cp_debug_email = 'emanuelguerrero@hotmail.com'; 

    //These would normally be loaded from your database, the most common way is to pass the Order ID through the 'custom' POST field. 
    $order_currency = 'DGB'; 
    $order_total = 0.01; 

	$file=fopen("datos.txt","a") or die("Problemas");

    function errorAndDie($error_msg) { 
        global $cp_debug_email; 
        if (!empty($cp_debug_email)) { 
            $report = 'Error: '.$error_msg."\n\n"; 
            $report .= "POST Data\n\n"; 
            foreach ($_POST as $k => $v) { 
                $report .= "|$k| = |$v|\n"; 
            } 
            #mail($cp_debug_email, 'CoinPayments IPN Error', $report); 
        } 
        die('IPN Error: '.$error_msg); 
    } 

    if (!isset($_POST['ipn_mode']) || $_POST['ipn_mode'] != 'hmac') { 
        errorAndDie('IPN Mode is not HMAC.'. fputs($file, "IPN Mode is not HMAC")); 
    } 

    if (!isset($_SERVER['HTTP_HMAC']) || empty($_SERVER['HTTP_HMAC'])) { 
        errorAndDie('No HMAC signature sent.' . fputs($file, "No HMAC signature sent.")); 
    } 

    $request = file_get_contents('php://input'); 
    if ($request === FALSE || empty($request)) { 
        errorAndDie('Error reading POST data.'. fputs($file, "Error reading POST data.")); 
    } 

    if (!isset($_POST['merchant']) || $_POST['merchant'] != trim($cp_merchant_id)) { 
        errorAndDie('No or incorrect Merchant ID passed' . fputs($file, "No or incorrect Merchant ID passed.")); 
    } 

    $hmac = hash_hmac("sha512", $request, trim($cp_ipn_secret)); 
    if (!hash_equals($hmac, $_SERVER['HTTP_HMAC'])) { 
    // if ($hmac != $_SERVER['HTTP_HMAC']) { 
        errorAndDie('HMAC signature does not match' . fputs($file, "HMAC signature does not match.")); 
      
     }
    // HMAC Signature verified at this point, load some variables. 

    $txn_id = $_POST['txn_id']; 
    $item_name = $_POST['item_name']; 
    $item_number = $_POST['item_number']; 
    $amount1 = floatval($_POST['amount1']); 
    $amount2 = floatval($_POST['amount2']); 
    $currency1 = $_POST['currency1']; 
    $currency2 = $_POST['currency2']; 
    $status = intval($_POST['status']); 
    $status_text = $_POST['status_text'];
    $invoice = $_POST['invoice'];



    
    
    
    
    fputs($file, $txn_id);
    fputs($file,"\n");
    fputs($file, $status);
    fputs($file,"\n");
    fputs($file, $status_text);
    fputs($file,"\n");
    fputs($file, $invoice);
    
    fputs($file,"\n");
    fputs($file, $hmac);
    
    fclose($file);

    
    

    //depending on the API of your system, you may want to check and see if the transaction ID $txn_id has already been handled before at this point 

    // Check the original currency to make sure the buyer didn't change it. 
    if ($currency1 != $order_currency) { 
        errorAndDie('Original currency mismatch!'); 
    }     
     
    // Check amount against order total 
    if ($amount1 < $order_total) { 
        errorAndDie('Amount is less than order total!'); 
    } 
   
    if ($status >= 100 || $status == 2) { 
        // payment is complete or queued for nightly payout, success 
    } else if ($status < 0) { 
        //payment error, this is usually final but payments will sometimes be reopened if there was no exchange rate conversion or with seller consent 
    } else { 
        //payment is pending, you can optionally add a note to the order page 
    } 
    die('IPN OK'); 