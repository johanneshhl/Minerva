	
	var dropZone = document.getElementById('dropzone');

	if (dropZone != null) {
		dropZone.addEventListener("dragenter", dragenter, false);
		dropZone.addEventListener("dragover", dragover, false);
		dropZone.addEventListener("drop", drop, true);
	};


	function dragenter(e) {
	  e.stopPropagation();
	  e.preventDefault();
	}
	
	function dragover(e) {
	  e.stopPropagation();
	  e.preventDefault();
	}

	function drop(e) {
	  e.stopPropagation();
	  e.preventDefault();
	 
		var dt = e.target.files||e.dataTransfer;
		var files = dt.files;
		var blob = files[0]; 

		var errorMessage = "Drag & Drop ➔ Input['type*='file'] er ikke supported på "

		if ((navigator.userAgent.indexOf('MSIE') !== -1 || navigator.appVersion.indexOf('Trident/') > 0)) {
			alert(errorMessage + 'Internet explore')

		}else if ((navigator.userAgent.indexOf('Firefox/')) !== -1) {
			alert(errorMessage + 'Firefox')
		}
		else{
	  		document.getElementById('selectedFile').files = files
	  		$('#selectedFile').change();
		};
	}



	function setValueOfInput(node, string) {
		if (string != 'None') {
			$(node).val(string);
		};
	}


	$("[data-function*='chooseFile']").click(function(event) {
		$("[name*='file']").click();
	});

	$('#selectedFile').change(function() {
		var FileStringLength = (($(this).val().split('\\').length) - 1)
		var docxTitle = $(this).val().split('\\')[FileStringLength]

	
		$('#dropzone').attr('data-text', 'Uploader');

		$.ajax({
				url: '/session/get_document_info',
				type: 'POST',
				dataType: 'iframe text',
				headers:{'Content-Type':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'},
				fileInputs: $(this)
				}).done(function(data){
					$('#dropzone').attr('data-text', docxTitle);
					$('#submitDocument').removeAttr('disabled');
					
					json = $.parseJSON(data);
					setValueOfInput('[name*="documentTitle"]', json.documnetName);
					setValueOfInput('[name*="documentSubtitle"]', json.documentSubtitle);
					setValueOfInput('[name*="documentSubject"]', json.documentSubject);
					setValueOfInput('[name*="documentTopic"]', json.documentTopic);
					setValueOfInput('[name*="documentDescription"]', json.documentDescription);

					if (json.documentEducation_level != '') {
						$('select[name*="documentEducation_level"]').children('option').prop('selected', true);
						$('select[name*="documentEducation_level"] option[value*="'+json.documentEducation_level+'"]').attr('selected', 'selected');
					}; 



				}).fail(function(){
					console.log(data)
		});


	});


	$("#submitDocument").click(function(event) {
		if ($(this).attr('disabled') != true) {
			$('#createDocument').submit();
		};
	});
	$("#submitDocument").click(function(event) {
		if ($(this).attr('disabled') != true) {
			$('#updateDocument').submit();
		};
	});

















		var toggle = document.getElementById('menu-toggle');
			var overlay = document.getElementById('overlay')
			
			if (toggle != null) {
			toggle.addEventListener('click', function() {
				var nameElem = document.getElementsByTagName("nav")[0]
				nameElem.classList.remove("close")
				nameElem.classList.add("open")

				document.getElementById('overlay').className = 'display'

			}, false);
			};	
			if (overlay != null) {
				overlay.addEventListener('click', function() {
					var nameElem = document.getElementsByTagName("nav")[0]
					nameElem.classList.remove("close")
					nameElem.classList.add("open")
	
					document.getElementById('overlay').className = 'display'
	
				}, false);
			};	

			var toggle = document.getElementById('menu-close');

			if (toggle != null) {
			toggle.addEventListener('click', function() {
				var nameElem = document.getElementsByTagName("nav")[0]
				nameElem.classList.remove("open")
				nameElem.classList.add("close")

				document.getElementById('overlay').className = 'hidden'

			}, false);
			};

			if (overlay != null) {

				overlay.addEventListener('click', function() {
					var nameElem = document.getElementsByTagName("nav")[0]
					nameElem.classList.remove("open")
					nameElem.classList.add("close")
					document.getElementById('overlay').className = 'hidden'

				}, false);
			};
			
				var search_toggle = document.getElementById('search_toggle');


				if (search_toggle != null) {
				var button = search_toggle.getElementsByTagName('span')[0];
				search_toggle.addEventListener('click', function() {

				var nameElem = document.getElementById('search_bar')

				if (button.classList[0] == 'icon-search'){
					button.className = 'icon-close';
				}else {
					button.className = 'icon-search';
				}


				if (nameElem.classList[2] == 'open') {
					nameElem.classList.remove('open')
					nameElem.classList.add("close")


				}else if (nameElem.classList[2] == 'close') {

					nameElem.classList.remove('close')
					nameElem.classList.add("open")



				}else if (nameElem.classList[2] != true) {
					nameElem.classList.add("open")

				};
				
				
			}, false);
			};



			if ($("[data-toggle*='list-view']") != null) {

					$("[data-toggle*='list-view']").on('click', function() {
						if ($(this).attr('class', 'active') != true){
							
							$(this).attr('class', 'active');
							$("[data-toggle*='document-view']").attr('class', null);
	
							var target = $(this).attr('data-target');
							var targetClass = $(this).attr('data-toggle');
							
							$(target).attr('class', targetClass);
	
						}
	
				});

			};

			if ($("[data-toggle*='document-view']") != null) {
				
				$("[data-toggle*='document-view']").on('click', function() {
					if ($(this).attr('class', 'active') != true){
						
						$(this).attr('class', 'active');

						$("[data-toggle*='list-view']").attr('class', null);

						var target = $(this).attr('data-target');
						var targetClass = $(this).attr('data-toggle');
						
						$(target).attr('class', targetClass);
					}

				});			
				
			};


				




function getUser(input) {
	var msg = $.ajax({
		type: "POST",
		url: '/session/checkuser',
		data: ({ email: input }),
		dataType: "text/html", async: false
	});

	return msg.responseText;
}


function validateUser (email) {
	var theTest = getUser(email)
	console.log(theTest)

	if (theTest === 'ok'){
		return true
	} 
	else{
		return false
	};
}

function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}

function validateString(string, length) {
	if (string.length <= length) {
		return false
	}else {
		return true
	}
}





$('[name*="email"]').keyup(function(event) {
	if ($(this).parents('form').attr('data-info') === 'createUserForm'){
		test = ((validateEmail(this.value) === true ) && (validateUser(this.value)) )
	} else {
		test = ((validateEmail(this.value) === true ))
	};
	validateInput(test, $(this))
});




$('[name*="firstname"]').keyup(function(event) {
	test = (validateString(this.value, 1) === true )
	validateInput(test, $(this))
});




$('[name*="lastname"]').keyup(function(event) {
	test = (validateString(this.value, 1) === true )
	validateInput(test, $(this))
});



$('[name*="password"]').keyup(function(event) {
	test = (validateString(this.value, 8) === true )
	validateInput(test, $(this))
});




function validateInput(functionVar, formElement) {
		
		
		var parentNode = formElement.parent('span');
		
		if (functionVar != true) {
			var codeClass = 'not_valid'

		}else {
			var codeClass = 'valid'
		}

		parentNode.attr('class', codeClass);

		var tests = ((formElement.parents('form').find('[name*="email"]').parent('span').attr('class') === 'valid') && formElement.parents('form').find('[name*="password"]').parent('span').attr('class') === 'valid')

		if (tests == true) {
			formElement.parents('form').find('button').removeAttr('disabled');
		} else {
			formElement.parents('form').find('button').attr('disabled', '');
		};

};







