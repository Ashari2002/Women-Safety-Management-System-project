import requests

def send_emergency_sms(phone_numbers, message):
    """
    Send SMS to emergency contacts using the BulkSMSBD API
    
    Args:
        phone_numbers: List of phone numbers to send SMS to
        message: The message to send
        
    Returns:
        tuple: (success_status, message)
    """
    # API credentials
    api_key = "dw532NCEiX3cFa8wUR4m"
    sender_id = "8809617625230"
    
    success_count = 0
    failed_numbers = []
    
    for phone in phone_numbers:
        # Construct the API URL
        api_url = f"http://bulksmsbd.net/api/smsapi"
        
        # Set up parameters
        params = {
            "api_key": api_key,
            "type": "text",
            "number": phone,
            "senderid": sender_id,
            "message": message
        }
        
        try:
            # Send the request
            response = requests.get(api_url, params=params)
            print(response.json())
            # Check if successful
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('status') == 'success':
                    success_count += 1
                else:
                    failed_numbers.append(phone)
            else:
                failed_numbers.append(phone)
                
        except Exception as e:
            failed_numbers.append(phone)
    
    # Return status summary
    if success_count == len(phone_numbers):
        return True, "SMS sent successfully to all contacts"
    elif success_count > 0:
        return True, f"SMS sent to {success_count} contacts. Failed for {len(failed_numbers)} contacts."
    else:
        return False, "Failed to send SMS to any contact"
    
send_emergency_sms(["01632495125", "01778501685", "01754739777"], "this is user")