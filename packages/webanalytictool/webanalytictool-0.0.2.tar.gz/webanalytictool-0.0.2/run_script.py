from src.analytic import WebPageAnalyticTool


url = 'file:///home/oyindolapo/Documents/PythonProjects/monetha/segmentation-model/segmentation-models/results/10/LTVcohorts_by_segments_relative.html'

wat = WebPageAnalyticTool(url)
tag = wat.get_all_tags()