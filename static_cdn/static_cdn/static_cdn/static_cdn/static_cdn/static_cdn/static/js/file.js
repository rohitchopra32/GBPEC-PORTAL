<script type="text/javascript">
	var fileInputTextDiv = document.getElementById("file_input_text_div");
	var fileInput = document.getElementById("file_input_file");
	var fileInputText = document.getElementById("file_input_text");
	fileInput.addEventListener("change", changeInputText);
	fileInput.addEventListener("change", changeState);	
	var old="";
	function changeInputText() {
	  var str = fileInput.value;
	  print(str)
	  var i;
	  if (str.lastIndexOf('\\'))
	   {
	   	i = str.lastIndexOf('\\') + 1;
	  } else if (str.lastIndexOf("/")) {
	    i = str.lastIndexOf("/") + 1;
	  }
	  old = old.concat(",",str.slice(i, str.length))
	  fileInputText.value = old;
	}
	function changeState() {
	  if (fileInputText.value.length != 0) {
	    if (!fileInputTextDiv.classList.contains("is-focused")) {
	      fileInputTextDiv.classList.add("is-focused");
	    }
	  } else {
	    if (fileInputTextDiv.classList.contains("is-focused")) {
	      fileInputTextDiv.classList.remove("is-focused");
	    }
	  }
	};
	</script>