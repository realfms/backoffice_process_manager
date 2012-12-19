	<?php
	function remoteRegister( $data = array() ) {
		// Generar un CASI-UUID como números incrementales
		// $contract_id = $bss_client_id = time();
		$contract_id = $bss_client_id = intval(microtime(TRUE)*10000);

		$postdata = array(
			'login'         => $data['login'],
			'name'          => $data['name'],
			'surname'       => $data['surname'],
			'email'         => $data['email'],
			'company'       => $data['company'],
			'phone'         => $data['phone'],
			'contract_id'   => $contract_id, 
			'bss_client_id' => $bss_client_id 
		); 

		$comando =  $this->_url;

		$curl = curl_init(); 
		curl_setopt($curl, CURLOPT_VERBOSE, $this->_verbose );

		curl_setopt($curl, CURLOPT_HTTPAUTH, CURLAUTH_BASIC ); 
		curl_setopt($curl, CURLOPT_USERPWD, $this->_userpwd); 
		curl_setopt($curl, CURLOPT_SSLVERSION,3); 
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, FALSE); 
		curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 2); 
		curl_setopt($curl, CURLOPT_HEADER, false);    
		 // Especificamos el content-type de la petición que obligatoriamente debe ser json
		curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json; charset=utf-8') );
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);     
		curl_setopt($curl, CURLOPT_URL, $comando); 
		curl_setopt($curl, CURLOPT_POST, true);
		$json = json_encode($postdata); 
		curl_setopt($curl, CURLOPT_POSTFIELDS, $json);


		$response 		= curl_exec($curl); 
		$requestinfo 	= curl_getinfo($curl);
		$http_code 		= intval( $requestinfo['http_code'] );
		/* para DEBUG activar y poner CUROPT_VERBOSE a true en las opciones curl
		echo "Código HTTP: $http_code<br />\n";
		echo "requestinfo<pre>" . print_r($requestinfo, true)."</pre><br />\n";
		echo "response<pre>" . print_r($response, true)."</pre><br />\n";
		*/
		if(in_array($http_code, array(200,202, 204) ) ){
			// Respuesta OK
			$resp = new ResponsePostCustomer($response);
			//echo "Status operación: {$resp->status}\n";
			if($resp->status === 0 ) {
				$this->error_msg = null;
				$this->customer_id = $resp->customer_id;
				return true;
			}
			
			// Si el status no es correcto no es un error subsanable por el usuario y generamos excepción
			throw new Exception("Error al crear el usuario remoto. El estado devuelto no es el esperado."
				. " Esperado = 0. Devuelto =  {$resp->status}. User ID={$resp->customer_id}" );

		} else {
			
			$res = new ErrorResponse( $response );
			// Si es un error 409 devolvemos un mensaje al usuario
			if($http_code == 409) {
				$this->error_msg[$res->parameter] = $res->reason;
				
				return false;

			}
			// Si es cualquier otro error el usuario no puede hacer nada y generamos excepción
			throw new Exception("Error in remote register PD1: {$res->code}, razon={$res->reason}" );
		}

	}
	?>