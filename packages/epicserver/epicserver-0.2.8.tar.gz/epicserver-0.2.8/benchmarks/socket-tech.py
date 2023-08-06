#!/usr/bin/env python
"""Its not enough to state somthing is faster, you have to prove it

as such here is a collection of ways to send messages and a framework 
to benchmark them

"There can only be one"
"""
from __future__ import print_function # Py3 compatibility
from time import time
from tempfile import mktemp
from multiprocessing import Queue, Event, Process as Thread
#from Queue import Queue
#from threading import Event, Thread
import socket
import sys
import os

def packet_generator(max_size=1500):
	from random import randrange as random

	while True:
		# binary data to play nice with py3k
		yield b" " * random(30, max_size)


class BenchReporter(object):
	def __init__(self, benchmarks):
		self.benchmarks = []
		for benchmark in benchmarks:
			self.add_benchmark(benchmark)

	def add_benchmark(self, benchmark):
		self.benchmarks.append(benchmark)

	def run(self):
		results = []
		for benchmark in self.benchmarks:
			results.append((benchmark.name, benchmark.run()))

		self.results = results

	def print_results(self):
		for name, results in self.results:
			runs = len(results)
			# in the data
			runtime = sum([x[0] for x in results]) / runs
			sent = sum([x[1] for x in results]) / runs
			recived = sum([x[2] for x in results]) / runs
			errors = sum([x[3] for x in results]) / runs
			# derived from the data
			lost = sent - recived
			lost_rate = float(lost) / runtime
			lost_percent = float(lost) / sent
			error_percent = float(errors) / sent
			error_rate = float(errors) / runtime
			connect_rate = float(recived) / runtime
			

			print(name.center(60, "-"))
			print("Completed {0} runs @ aproximatly {1:.3f} seconds each".format(runs, runtime))
			print("Sent {0:.0f} packets, Recived {1:.0f} packets ({2:.2f} connections/sec)".format(sent, recived, connect_rate))
			print("lost {0:.0f} ({1:.1%}) packets @ {2:.2f}/s)".format(lost, lost_percent, lost_rate))
			print("{0} errors ({1:.1%} @ {2:.2f}/s)".format(errors, error_percent, error_rate))
			print()

class BenchRunner(object):
	def __init__(self, name, benchmark, count=3, messages=10000, packet_gen=packet_generator):
		self.benchmark = benchmark
		self.count = count
		self.name = name
		self.messages = messages
		self.packet_gen = packet_gen

	def run(self):
		results = []
		self.benchmark.setup()
		self.benchmark.run(self.messages, self.packet_gen)
		for i in range(self.count):
			results.append(self.benchmark.run(self.messages, self.packet_gen))
		self.benchmark.teardown()

		return results

	def __str__(self):
		return self.name

class SocketConnection(object):
	"""ABC for benchmarks

	the user must implement a setup and teardown (if applicable) as well
	as putting the actual code in the benchmark

	*** Note *** the class is "warmed up" and the first couple of results
	discarded
	"""
	def setup(self):
		"""Setup code required for a benchmark run that is not part
		of the benchmark process itself, normmaly connection 
		initalisation"""
		pass

	def run(self, messages, data):
		"""benchmark setup and run code

		Messages indicates the ammount of messages to send/recive
		data is a generator of packets, length may be varible

		Returns a 3 valued tuple of the ammount of messages sent,
		the ammount of messages recived and the ammount of errors
		(on both the send and recive end added together)
		any message that errors on being sent does not increment the
		send count, the same applies for the recive end
		"""
		queue = Queue()
		start_barrier = Event()
		# binary data to play nice with py3k
		sentinal = b"Die Die Die!!!"

		send_thread = Thread(None, self._send_all, args=(queue, start_barrier, messages, data, sentinal))
		recv_thread = Thread(None, self._recv_all, args=(queue, start_barrier, sentinal))

		send_thread.start()
		recv_thread.start()
		
		start_time = time()

		start_barrier.set()
		send_thread.join()
		recv_thread.join()

		end_time = time()

		recived = 0
		sent = 0
		send_errors = 0
		recv_errors = 0
		# warning, double check this works (read queue.empty docstrings)
		while not queue.empty():
			t, stats = queue.get()
			if t == "recv":
				recived, recv_errors = stats
			else:
				sent, send_errors = stats

		run_time = end_time - start_time

		return (run_time, sent, recived, send_errors + recv_errors)

	def teardown(self):
		"""Any post processing required (eg shuttong down connections)
		that may be required by the class"""
		pass

	def _send_all(self, queue, start_lock, messages, data, sentinal):
		# wait on lock
		start_lock.wait()
		stats = self.send_all(messages, data, sentinal)
		queue.put(("send", stats))

	def send_all(self, messages, data, sentinal):
		"""A function for sending all the packets

		Used to split the benchmark into 2 threads
		for more information see self.benchmark and self.recv_all
		"""
		pass

	def _recv_all(self, queue, start_lock, sentinal):
		start_lock.wait()
		stats = self.recv_all(sentinal)
		queue.put(("recv", stats))

	def recv_all(self, sentinal):
		"""A function for recving all the packets

		Used to split the benchmark into 2 threads
		for more information see self.benchmark and self.recv_all
		"""
		pass

class SockConnection(SocketConnection):
	"""UDP over IPv4 Connection"""
	def __init__(self, family, typ, address):
		self.family = family
		self.typ = typ
		self.address = address

	def setup(self):
		send_sock = socket.socket(self.family, self.typ)
		recv_sock = socket.socket(self.family, self.typ)

		recv_sock.bind(self.address)
		# Connection based sockets only
		#recv_sock.listen(200)

		send_sock.connect(self.address)

		self.send_sock = send_sock
		self.recv_sock = recv_sock

	def send_all(self, messages, data, sentinal):
		sent = 0
		errors = 0
	
		# prep generator
		data = data()
		next(data)

		for i in range(messages):
			try:
				self.send_sock.send(next(data))
				sent += 1
			except socket.error:
				errors += 1
		self.send_sock.send(sentinal)

		return sent, errors

	def recv_all(self, sentinal):
		recived = 0
		errors = 0
		while True:
			try:
				data = self.recv_sock.recv(3000)
				if data[:len(sentinal)] == sentinal:
					break
				recived += 1
			except socket.error:
				errors += 1

		return recived, errors

	def teardown(self):
		self.send_sock.close()
		self.recv_sock.close()


if __name__ == "__main__":
	unix_loc = mktemp()
	tests = []
	tests.append(("IPV4 UDP Connection Test", SockConnection(socket.AF_INET, socket.SOCK_DGRAM, ("localhost", 9000))))
	tests.append(("IPV6 UDP Connection Test", SockConnection(socket.AF_INET6, socket.SOCK_DGRAM, ("localhost", 9000))))
	tests.append(("Unix Socket Connection Test", SockConnection(socket.AF_UNIX, socket.SOCK_DGRAM, unix_loc)))

	tests = [BenchRunner(*x) for x in tests]

	results = BenchReporter(tests)

	results.run()

	results.print_results()

	os.unlink(unix_loc)
