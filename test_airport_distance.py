import unittest
import airport_distance
import mock
import pandas
import networkx


class MyTestCase(unittest.TestCase):
	@mock.patch('airport_distance.pd.read_csv')
	def test_getting_graph(self, df):
		df.return_value = pandas.DataFrame([{"Dep": "DUB", "Arr": "LAX", "Time": 1}])
		graph = airport_distance.read_in_graph("test_path")
		expected_nodes = ['DUB', 'LAX']
		self.assertListEqual(expected_nodes, list(graph.nodes()))

	@mock.patch('airport_distance.input')
	def test_getting_input_with_good_input(self, good_input):
		good_input.return_value = "DUB -- LAX"
		dep, arr = airport_distance.read_in_airports(["DUB", "LAX"])
		self.assertEqual("DUB", dep)
		self.assertEqual("LAX", arr)

	@mock.patch('airport_distance.print')
	@mock.patch('airport_distance.input')
	def test_input_retry_with_bad_input_value(self, inputs, print):
		inputs.side_effect = [" NOTAGOODVAL", "DUB -- LAX"]
		dep, arr = airport_distance.read_in_airports(["DUB", "LAX"])
		self.assertEqual(2, inputs.call_count)
		self.assertEqual(1, print.call_count)
		self.assertTrue("Unable to parse" in print.call_args.args[0])

	@mock.patch('airport_distance.print')
	@mock.patch('airport_distance.input')
	def test_input_retry_with_bad_arrival_value(self, inputs, print):
		inputs.side_effect = ["SAX -- LAX", "DUB -- LAX"]
		dep, arr = airport_distance.read_in_airports(["DUB", "LAX"])
		self.assertEqual(2, inputs.call_count)
		self.assertEqual(1, print.call_count)
		self.assertTrue("departure airport" in print.call_args.args[0])


	@mock.patch('airport_distance.print')
	@mock.patch('airport_distance.input')
	def test_input_retry_with_bad_departure_value(self, inputs, print):
		inputs.side_effect = ["DUB -- SAX", "DUB -- LAX"]
		dep, arr = airport_distance.read_in_airports(["DUB", "LAX"])
		self.assertEqual(2, inputs.call_count)
		self.assertEqual(1, print.call_count)
		self.assertTrue("destination airport" in print.call_args.args[0])


	@mock.patch('airport_distance.print')
	@mock.patch('airport_distance.input')
	def test_input_retry_with__bad_departure_and_bad_arrival_value(self, inputs, print):
		inputs.side_effect = ["HAS -- SAX", "DUB -- LAX"]
		dep, arr = airport_distance.read_in_airports(["DUB", "LAX"])
		self.assertEqual(2, inputs.call_count)
		self.assertEqual(1, print.call_count)
		self.assertTrue("destination airport" in print.call_args.args[0])
		self.assertTrue("departure airport" in print.call_args.args[0])

	def test_get_shortest_path(self):
		G= networkx.DiGraph()
		G.add_edge("DUB", "LAX", Time=5)
		len, path = airport_distance.get_shortest_path(G, "DUB", "LAX")
		self.assertEqual(5, len)
		self.assertEqual(["DUB", "LAX"], path)

	def test_get_shortest_path_no_dep(self):
		G= networkx.DiGraph()
		G.add_edge("DUB", "LAX", Time=5)
		len, path = airport_distance.get_shortest_path(G, "HAS", "LAX")
		self.assertEqual(None, len)
		self.assertEqual(None, path)

	def test_get_shortest_path_no_arr(self):
		G = networkx.DiGraph()
		G.add_edge("DUB", "LAX", Time = 5)
		len, path = airport_distance.get_shortest_path(G, "DUB", "HAS")
		self.assertEqual(None, len)
		self.assertEqual(None, path)

	def test_format_output(self):
		len = 7
		path = ["DUB", "LAX", "HAR"]
		G = networkx.DiGraph()
		G.add_edge("DUB", "LAX", Time = 5)
		G.add_edge("LAX", "HAR", Time = 2)
		expected_output = """DUB -- LAX (5) \nLAX -- HAR (2) \ntime: 7"""
		res = airport_distance.format_output(G, len, path)
		self.assertEqual(expected_output, airport_distance.format_output(G, len, path))

	@mock.patch('airport_distance.print')
	@mock.patch('airport_distance.pd.read_csv')
	@mock.patch('airport_distance.input')
	def test_calulate_shortest_path_good_path(self, input, df, print):
		df.return_value = pandas.DataFrame([{"Dep": "DUB", "Arr": "LAX", "Time": 1}])
		input.return_value = "DUB -- LAX"
		expected_output = """DUB -- LAX (1) \ntime: 1"""
		airport_distance.calculate_shortest_path("test_filename_is_ignored")
		print.assert_called_with(expected_output)


if __name__ == '__main__':
	unittest.main()
