"""Analyzes the script for out of bounds bounding boxes and too many layers
"""

import nuke
from os import system


def checkEfficiency(startNode = None):
	""" CheckEfficiency UI
			Arg: 
				startNode : analyze all nuke nodes connected to this nodes
	"""

	try:
		if not startNode:
			startNode = nuke.selectedNode()
	except ValueError:
		msg = "No start node selected"
		nuke.message(msg)
		return

	formatWeight = nuke.Root().format().width() * nuke.Root().format().height()

	analyzeBBox = True
	bboxThreshold = 300
	analyzeLayers = True
	layerThreshold = 6

	panel = nuke.Panel('Efficiency Checker')
	panel.addBooleanCheckBox('Analyze Bounding Box', analyzeBBox)
	panel.addBooleanCheckBox('Analyze Layers', analyzeLayers)
	panel.addSingleLineInput('Bounding Box Threshold', bboxThreshold)
	panel.addSingleLineInput('Layer Threshold', layerThreshold)
	panel.addButton('Cancel')
	panel.addButton('Analyze')
	panel.addButton('Revert Node Colors')
	panel.addButton('Help')

	result = panel.show()

	nodes = nuke.selectConnectedNodes()
	nodes = nuke.selectedNodes()
	[node['selected'].setValue(False) for node in nodes]
	startNode['selected'].setValue(True)

	# Analyze
	if result == 1:
		analyzeBBox = panel.value('Analyze Bounding Box')
		bboxThreshold = float(panel.value('Bounding Box Threshold')) / 100
		analyzeLayers = panel.value('Analyze Layers')
		layerThreshold = int(panel.value('Layer Threshold'))

		nodeInfos = _analyzeNodes(nodes, analyzeBBox, analyzeLayers)
		_setColors(nodeInfos, formatWeight, analyzeBBox, analyzeLayers, bboxThreshold, layerThreshold)

	# Revert
	elif result == 2:
		_revertColors(nodes)

	# Help (some sort of wiki link / or a popup with an image?)
	elif result == 3:
		print "To be completed.."

	# Cancel
	elif result == 0:
		return

def _revertColors(nodes):
	"""Revert Node color to default
		Arg: 
			nodes: list of Nuke nodes 
	"""
	for node in nodes:
		node['tile_color'].setValue(0)

def _isDeep(node):
	"""Check to see if the node is a deep node
		Arg:
			node: Nuke node
	"""
	try:
		node.deepSampleCount(0, 0)
		return True
	except ValueError:
		return False

def _analyzeNodes(nodes, analyzeBBox, analyzeLayers):
	"""Process upstream from a selected node recursively. 
		if a deep node is detected, place 'DeepToImage' node to gather bbox nodeInfos
		Args:
			nodes: list of nuke nodes
			analyzeBBox (bool): perform bbox check
			analyzeLayers (bool): perform layer check
		Returns:
			nodeInfos (dict of dicts): bbox size and the number of layers per nuke node
	"""

	task = nuke.ProgressTask('Analyzing...')
	increment = 100.0 / len(nodes)
	progress = 0
	nodeInfos = {}

	for node in nodes:
		progress += 1
		task.setProgress(int(progress * increment))
		task.setMessage(node.name())
		if task.isCancelled():
			return
		nodeInfos[node] = {}

		if analyzeBBox:
			if _isDeep(node):
				deepToImage = nuke.nodes.DeepToImage(inputs = [node,])
				bboxWeight = deepToImage.bbox().w() * deepToImage.bbox().h()
				nuke.delete(deepToImage)
			else:
				bboxWeight = node.bbox().w() * node.bbox().h()
			nodeInfos[node]['bbox'] = bboxWeight

		if analyzeLayers:
			layers = [layer.split('.')[0] for layer in node.channels()]
			layers = len(set(layers))
			nodeInfos[node]['layers'] = layers

	return nodeInfos

def _setColors(nodeInfos, formatWeight, analyzeBBox, analyzeLayers, bboxThreshold, layerThreshold):
	""" Change colors of the node based on the number of layers and size of the bbox
		Args:
			nodeInfos (dict of dicts) : bbox size and the number of layers per nuke node
			formatWeight (int) : number of pixels in Nuke;s root format
			analyzeBBox (bool) : perform bbox check
			analyzeLayers (bool) : perform layer check
			bboxThreshold (float) : bbox limit
			layerThreshold (int) : layer number limit
	"""

	task = nuke.ProgressTask('Setting colors...')
	increment = 100.0 / len(nodeInfos)
	progress = 0

	for node, nodeInfo, in nodeInfos.iteritems():
		progress += 1
		task.setProgress(int(progress * increment))
		task.setMessage(node.name())
		if task.isCancelled():
			_revertColors(nodeInfos.keys())

		brightness = 1
		hue = 1
		red = 1
		green = 1
		blue = 0

		if analyzeLayers:
			brightness = min(1, (1 - min(1, nodeInfo['layers'] / float(layerThreshold))) + 0.3)

		if analyzeBBox:
			hue = min(1, nodeInfo['bbox'] / formatWeight / bboxThreshold)
			green = 1 - hue

		red = hue* brightness
		green *= brightness

		colorHex = int('%02x%02x%02x%02x' % (red*255, green*255, blue*255, 1), 16)
		node['tile_color'].setValue(colorHex)

#checkEfficiency.checkEfficiency()