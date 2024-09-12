# __pragma__ ('skip')
def require(lib):
	return lib


class document:
	getElementById = None
	addEventListener = None


# __pragma__ ('noskip')

# Load React and ReactDOM JavaScript libraries into local namespace
React = require("react")
ReactDOMClient = require("react-dom/client")

# Map React javaScript objects to Python identifiers
createElement = React.createElement
useState = React.useState


def render(root_component, props, container):
	"""Loads main react component into DOM"""

	def main():
		domNode = document.getElementById(container)
		root = ReactDOMClient.createRoot(domNode)
		root.render(React.createElement(root_component, props))

	document.addEventListener("DOMContentLoaded", main)
