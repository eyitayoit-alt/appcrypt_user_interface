from react import useState, render, createElement as el


def App():
	# State management
	selectOption, setSelectOption = useState("Encrypt")
	filePath, setFilePath = useState("")
	keyPath, setKeyPath = useState("")
	uploadFile, setFile = useState()
	keyFile, setKeyFile = useState()
	error, setError = useState("")

	# Handlers
	def handleSelect(event):
		setSelectOption(event.target.value)
		setFilePath("")
		setKeyPath("")

	def handleFileSelection(event):
		file = event.target.files[0]
		setFile(file)

	def handleKeySelection(event):
		kFile = event.target.files[0]

		setKeyFile(kFile)

	async def handleSubmit(event):
		event.preventDefault()
		formData = __new__(FormData())
		formData.append("file", uploadFile)
		formData.append("type", selectOption)
		if selectOption == "Encrypt":
			url = "http://127.0.0.1:8000/encodefile"
		else:
			url = "http://127.0.0.1:8000/decodefile"
			formData.append("keyfile", keyFile)
		event.target.reset()
		try:
			result = await fetch(url, {"method": "POST", "mode": "cors", "body": formData})
			if result.ok:
				data = await result.json()
				setFilePath(data.filepath)
				setKeyPath(data.keypath)
			else:
				setError(f"An error occurred: {result.status}")
		except Exception as err:
			setError(f"Unexpected error: {err}")

	# Render functions
	def renderDownloadLinks():
		if filePath:
			links = [
				el(
					"a",
					{"href": f"http://127.0.0.1:8000/download{filePath}"},
					f"Download {selectOption}ed File",
				)
			]
			if selectOption == "Encrypt" and keyPath:
				links.append(
					el(
						"a",
						{"href": f"http://127.0.0.1:8000/download{keyPath}"},
						"Download Encryption Key",
					)
				)
			return el("div", {"className": "path-text"}, *links)

	def renderForm():
		inputs = [
			el(
				"label",
				{"htmlFor": "file-input"},
				f"Select file to be {selectOption.lower()}ed",
			),
			el(
				"input",
				{
					"type": "file",
					"id": "file-input",
					"accept": [".pdf", ".jpeg", ".png", ".doc", ".txt"],
					"required": True,
					"onChange": handleFileSelection,
				},
			),
		]
		if selectOption == "Decrypt":
			inputs.extend(
				[
					el("label", {"htmlFor": "key-input"}, "Select Encryption Key"),
					el(
						"input",
						{
							"type": "file",
							"id": "key-input",
							"required": True,
							"accept": ".key",
							"onChange": handleKeySelection,
						},
					),
				]
			)
		return el(
			"form",
			{
				"onSubmit": handleSubmit,
				"name": "appForm",
				"className": f"{selectOption.lower()}Form",
			},
			*inputs,
			el("button", {"type": "submit", "className": "form-button"}, "Start"),
		)

	def renderInstruction():
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
					"To encrypt a file, select Encryption. Choose a file (Pdf/Docs/Txt/Jpeg). Click the start Button.",
					el("br", {}),
					"To decrypt a file encrypted by this app, select Decryption, choose the file, then select the encryption key. Click the start button.",
				),
				renderDownloadLinks(),
			),
		)

	def renderApp():
		return el(
			"div",
			{"className": "main"},
			renderInstruction(),
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
						"checked": selectOption == "Encrypt",
					},
				),
				el("label", {"htmlFor": "decrypt"}, "Decryption"),
				el(
					"input",
					{
						"type": "radio",
						"onChange": handleSelect,
						"id": "decrypt",
						"value": "Decrypt",
						"name": "AppEncrypt",
						"checked": selectOption == "Decrypt",
					},
				),
			),
			renderForm(),
		)

	return renderApp()


render(App, None, "root")
