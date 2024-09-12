from react import useState, render, createElement as el


def App():
	selectOption, setSelectOption = useState("Encrypt")
	filePath, setFilePath = useState("")
	keyPath, setKeyPath = useState("")
	fileName, setFileName = useState([])
	uploadfile, setFile = useState()
	keyfile, setKeyFile = useState()
	error, setError = useState("")

	def handleSelect(event):
		setSelectOption(event.target.value)

	def handleFileSelection(event):
		file = event.target.files[0]
		setFileName(file["name"])
		setFile(file)

	def handleKeySelection(event):
		kFile = event.target.files[0]
		setFileName(fileName + " ," + kFile["name"])
		setKeyFile(kFile)

	def displayUploadedFiles():
		return el("div", {}, el("p", {}, fileName))

	def downloadPath():
		if filePath:
			if selectOption == "Encrypt":
				return el(
					"div",
					{"className": "path-text"},
					el(
						"p",
						{},
						"Your " + selectOption + "ed file and is avaliaible at",
						el(
							"a",
							{"href": "http://127.0.0.1:8000/download" + filePath},
							"Download Encrypted File",
						),
						"and the Encryption key at",
						el(
							"a",
							{"href": "http://127.0.0.1:8000/download" + keyPath},
							"Download Encryption key",
						),
					),
				)
			else:
				return el(
					"div",
					{"className": "path-text"},
					el(
						"p",
						{},
						"Your " + selectOption + "ed file and is avaliaible at",
						el(
							"a",
							{"href": "http://127.0.0.1:8000/download" + filePath},
							"Download" + selectOption + "ed File",
						),
					),
				)

	async def handleSubmit(event):
		event.preventDefault()
		formData = __new__(FormData())
		if selectOption == "Encrypt":
			formData.append("file", uploadfile)
			formData.append("type", selectOption)
			setFileName("")
			try:
				result = await fetch(
					"http://127.0.0.1:8000/encodefile",
					{"method": "POST", "mode": "cors", "body": formData},
				)
				if result.ok:
					data = await result.json()
					setFilePath(data.filepath)
					setKeyPath(data.keypath)
				else:
					setError("An Error occurred" + result.status)
			except Exception as err:
				console.log(err)

		else:
			formData.append("type", selectOption)
			formData.append("file", uploadfile)
			formData.append("keyfile", keyfile)
			setFileName("")
			try:
				result = await fetch(
					"http://127.0.0.1:8000/decodefile",
					{"method": "POST", "mode": "cors", "body": formData},
				)
				if result.ok:
					data = await result.json()
					setFilePath(data.filepath)
				else:
					setError("An error occurred" + result.status)
			except Exception as err:
				print(f"Unexpected {err=}, {type(err)=}")

	def encryptForm():
		return el(
			"form",
			{"onSubmit": handleSubmit, "className": "encryptForm"},
			el("h3", {}),
			el("label", {"htmlFor": "file-input"}, "Select File to be Encrypted"),
			el(
				"input",
				{
					"type": "file",
					"id": "file-input",
					"accept": [".pdf", ".jpeg", ".png", "doc", "txt"],
					"name": "inputfile",
					"onChange": handleFileSelection,
				},
			),
			el("p", {}, fileName),
			el("button", {"type": "submit", "className": "form-button"}, "Start"),
		)

	def decryptForm():
		return el(
			"form",
			{"onSubmit": handleSubmit, "className": "decryptForm"},
			el("h3", {}),
			el("label", {"htmlFor": "file-input"}, "Select file to be decrypted"),
			el(
				"input",
				{
					"type": "file",
					"id": "file-input",
					"name": "inputfile",
					"accept": [".pdf", ".jpeg", ".png", "doc", "txt"],
					"onChange": handleFileSelection,
				},
			),
			el("label", {"htmlFor": "key-input"}, "Select Encryption Key"),
			el(
				"input",
				{
					"type": "file",
					"id": "key-input",
					"name": "keyfile",
					"accept": ".key",
					"onChange": handleKeySelection,
				},
			),
			el("button", {"type": "submit", "className": "form-button"}, "Start"),
		)

	def instructionContainer():
		return el(
			"div",
			{"className": "container"},
			el("h2", {"className": "AppHeader"}, "File Encryption and Decryption App"),
			el("p", {}, error),
			el(
				"div",
				{"className": "instruction"},
				el("h3", None, "Instructions"),
				el(
					"p",
					None,
					"To encrypt a file, seclect Encryption. Choose a file(Pdf/Docs/Txt/Jpeg).Click the start Button.",
					el("br", {}),
					"To decrypt a file, encrypted by this app, Select decryption, select the file, select the encryption .key file. Click the start button",
				),
			),
			el(downloadPath),
		)

	def container():
		if selectOption == "Encrypt":
			return el("div", {}, el(displayUploadedFiles), el(encryptForm))
		else:
			return el("div", {}, el(displayUploadedFiles), el(decryptForm))

	return el(
		"div",
		{"className": "main"},
		el(instructionContainer),
		el(
			"div",
			{"className": "selectionContainer"},
			el("label", {"htmlFor": "encrypt"}, "Encryption"),
			el(
				"input",
				{
					"type": "radio",
					"onChange": handleSelect,
					"id": "encrypt",
					"value": "Encrypt",
					"name": "AppEncrypt",
					"checked": True,
				},
			),
			el("label", {"htmlFor": "decrypt"}, "Decrypt"),
			el(
				"input",
				{
					"type": "radio",
					"onChange": handleSelect,
					"value": "Decrypt",
					"id": "decrypt",
					"name": "AppEncrypt",
				},
			),
		),
		el(container),
	)


render(App, None, "root")
