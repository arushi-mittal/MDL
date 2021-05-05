import numpy as np
import client
import random
import sys
import json

popsize = 16 #population size subject to change
key = "z8l1kyoOkLgWkz8cL5tGtST2IXcsNMw8c52RaIHSNqiNeOHDdj"
k = 6
mut_range = 0.10
mut_prob = 0.4
iterations = 3

gen_original_pop = []
gen_parents = []
gen_crossover_children = []
gen_mutated_children = []

def mutate(arr, prob, mrange):
	for i in range(len(arr)):
		val = np.random.uniform(-mrange, mrange)
		if(arr[i] == 0.00000000e+00):
			val = random.uniform(-1e-11, 1e-11)
			arr[i] = np.random.choice([arr[i] + val, arr[i]], p=[prob, 1-prob])
		else:
			arr[i] = np.random.choice([(arr[i]*val) + arr[i], arr[i]], p=[prob, 1-prob])
		if(arr[i] > 10):
			arr[i] = 10
		elif(arr[i] < -10):
			arr[i] = -10

	return arr 

#simulated binary crossover
def crossover(parent1, parent2):
	child1 = np.zeros(11)
	child2 = np.zeros(11)
	parent1 = np.array(parent1)
	parent2 = np.array(parent2)

	n = 3

	u = random.random()
	if(u <= 0.5):
		b = (2*u)**(1/(n + 1))
	else:
		b = (1/(2*(1 - u)))**(1/(n + 1))

	child1 = 0.5*((1 + b) * parent1 + (1 - b) * parent2)
	child2 = 0.5*((1 - b) * parent1 + (1 + b) * parent2)

	return child1, child2

def generations () :
	for i in range (1, iterations+1):
		filename = "diagram_"+str(i)+".txt"
		f = open(filename, "w")
		f.write("Original Population: ")
		f.write(str(gen_original_pop[i - 1]))
		f.write("\n")
		f.write("Parents: ")
		f.write(str(gen_parents[i - 1]))
		f.write("\n")
		f.write("Crossover Children: ")
		f.write(str(gen_crossover_children[i - 1]))
		f.write("\n")
		f.write("Mutated Children: ")
		f.write(str(gen_mutated_children[i - 1]))
		f.close()


def main():
	#initial_vector = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]
	#initial_vector = np.array(initial_vector)
	population = np.zeros((popsize, 11))
	original_population = np.zeros((popsize, 11))
	errors = np.zeros(popsize)
	errors1 = np.zeros(popsize)
	errors2 = np.zeros(popsize)
	child_errors = np.zeros(k)
	child_errors1 = np.zeros(k)
	child_errors2 = np.zeros(k)

	#generate the initial population
	#for i in range(popsize):
	#	population[i] = mutate(initial_vector, 0.9, mut_range)

	population = np.copy([[-2.1979127752353937e-12, -2.026467870191969e-12, -2.3404723082751514e-13, 4.591932205334458e-11, -5.2509248544757e-11, -1.1790963051945611e-15, 9.574997365652972e-16, 2.3969698057747152e-05, -1.6737692764075557e-06, -1.4590575921693647e-08, 7.766118028201611e-10], [-2.1633841966501003e-12, -2.2545731851188725e-12, -2.423145404694651e-13, 4.806795894791935e-11, -5.3640045912088694e-11, -1.1790963051945611e-15, 1.0022849509638359e-15, 2.396969805774715e-05, -1.673769276407556e-06, -1.4590575921693647e-08, 7.76611802820161e-10], [-2.197447526538208e-12, -2.183491606425423e-12, -2.340620550875386e-13, 4.815374426801597e-11, -5.368519351909754e-11, -1.1790963051945611e-15, 9.529137486438568e-16, 2.396969805774715e-05, -1.6737692764075557e-06, -1.4590575921693646e-08, 7.76611802820161e-10], [-2.3912197686879736e-12, -2.2927152095020196e-12, -2.2879807724889627e-13, 4.79888088518559e-11, -5.550352995543773e-11, -1.1790963051945611e-15, 1.0514653087469206e-15, 2.3969698057747145e-05, -1.673769276407556e-06, -1.4590575921693646e-08, 7.766118028201611e-10], [-2.1981531175953147e-12, -2.0265124359688085e-12, -2.3472698691188633e-13, 4.585548523696718e-11, -5.624523458939281e-11, -1.1790963051945611e-15, 1.0250179624645082e-15, 2.396969805774715e-05, -1.6737692764075557e-06, -1.4590575921693646e-08, 7.76611802820161e-10], [-2.1980409334027405e-12, -2.246531342698275e-12, -2.2505705816718188e-13, 4.801834040536189e-11, -5.6289465463228505e-11, -1.1790963051945611e-15, 1.024663828780703e-15, 2.396969805774715e-05, -1.6737692764075557e-06, -1.4590575921693646e-08, 7.76611802820161e-10], [-2.392340768948038e-12, -2.294260859031194e-12, -2.2876365230167475e-13, 4.800119553963215e-11, -5.5499223405949e-11, -1.1063069572876672e-15, 1.0959073175911582e-15, 2.396969805774715e-05, -1.6737692764075562e-06, -1.4765469346649082e-08, 7.766118028201612e-10], [-2.2146607183639086e-12, -2.2445600804526126e-12, -2.3298832007325577e-13, 4.8080043336093405e-11, -5.3646405755563195e-11, -1.1790963051945611e-15, 9.953301389659054e-16, 2.4906746303516258e-05, -1.6737692764075557e-06, -1.4781464710893071e-08, 7.309512039608373e-10], [-2.0903879868954033e-12, -2.2457776757976275e-12, -2.1562614767156933e-13, 4.801995921621891e-11, -5.6258330282775324e-11, -1.1251184108039062e-15, 9.360478325260698e-16, 2.3969698057747145e-05, -1.6737692764075557e-06, -1.3417703331811415e-08, 7.276540027476406e-10], [-2.207906061715735e-12, -2.0399599203493415e-12, -2.3448116356491637e-13, 4.405033905006161e-11, -5.3394740862778736e-11, -1.16995475047025e-15, 1.0263539751262805e-15, 2.396969805774715e-05, -1.6737692764075557e-06, -1.4590575921693644e-08, 7.172249158312108e-10], [-2.3073643351096137e-12, -2.062506339303927e-12, -2.2811920252484314e-13, 4.625878623629341e-11, -5.268790376814592e-11, -1.1790963051945611e-15, 9.645753742648893e-16, 2.3969698057747152e-05, -1.8260715279260443e-06, -1.4590575921693647e-08, 7.766118028201611e-10], [-2.1926491006489646e-12, -2.1935047110916828e-12, -2.547024548646736e-13, 4.540964556241079e-11, -5.367883367562304e-11, -1.1790963051945611e-15, 9.584517029596301e-16, 2.396969805774715e-05, -1.6737692764075557e-06, -1.4590575921693646e-08, 7.056454933975837e-10], [-2.2870701007174074e-12, -2.2185347160069147e-12, -2.373960366579039e-13, 4.416767921167938e-11, -5.502156681823769e-11, -1.1790963051945611e-15, 9.93828797999289e-16, 2.396969805774715e-05, -1.673769276407556e-06, -1.6022293801109776e-08, 7.219809685236768e-10], [-2.381466824567553e-12, -2.174737518640329e-12, -2.290975817169694e-13, 4.78810419957519e-11, -6.03523777013701e-11, -1.2374723291153843e-15, 1.0501292960851483e-15, 2.226162549360819e-05, -1.8319154095185774e-06, -1.4590575921693644e-08, 7.766118028201611e-10], [-2.197454620970051e-12, -2.18424527332607e-12, -2.5295023986132457e-13, 4.815212545715895e-11, -5.740879185623374e-11, -1.1790963051945611e-15, 9.537715514158083e-16, 2.2852690573656853e-05, -1.6737692764075557e-06, -1.4590575921693646e-08, 8.399968635931893e-10], [-2.1970321173352507e-12, -2.024966786439635e-12, -2.206162461772447e-13, 4.5843098549190934e-11, -5.6249541138881557e-11, -1.2571005763362954e-15, 9.48464857025232e-16, 2.4481390682614638e-05, -1.5141194053745652e-06, -1.4590575921693647e-08, 7.766118028201611e-10]])
	original_population = np.copy(population)
	
	#random.seed()
	factor = 2000
	#print(factor)
	#print("\n")
	#generate errors for every individual in population
	for i in range(popsize):
		#passing the inidividual to get_errors function
			
		err = client.get_errors(key, population[i].tolist())
		#for now, error=err[0]+err[1] but might change weightages later
		errors[i] = np.copy(err[0]+err[1]+factor*(abs(err[0]-err[1])))
		errors1[i] = np.copy(err[0])
		errors2[i] = np.copy(err[1])
		
	indices = np.zeros(popsize)
	temp_population = np.zeros((popsize, 11))
	temp_errors = np.zeros(popsize)
	temp_errors1 = np.zeros(popsize)
	temp_errors2 = np.zeros(popsize)

	#fitness = 1/error, so sorting in ascending error
	indices = np.copy(np.argsort(errors))
	temp_population = np.copy(population)
	temp_errors = np.copy(errors)
	temp_errors1 = np.copy(errors1)
	temp_errors2 = np.copy(errors2)
	for i in range(popsize):
		population[i] = np.copy(temp_population[indices[i]])
		errors[i] = np.copy(temp_errors[indices[i]])
		errors1[i] = np.copy(temp_errors1[indices[i]])
		errors2[i] = np.copy(temp_errors2[indices[i]])

	for x in range(iterations):

		#print("Iteration: ",x)

		#now parents have been sorted acc to fitness
		gen_original_pop.append(population)

		parent1 = np.zeros(11)
		parent2 = np.zeros(11)
		child1 = np.zeros(11)
		child2 = np.zeros(11)

		x2 = 0
		parents = np.zeros((k, 11))
		unmutated_children = np.zeros((popsize-k, 11))
		#taking top k individuals as parents
		parents = np.copy(population[:k])

		gen_parents.append(parents)

		child_population = np.zeros((popsize-k, 11))
		child_errors = np.zeros(popsize-k)
		child_errors1 = np.zeros(popsize-k)
		child_errors2 = np.zeros(popsize-k)
		gen_crossover_children.append([])
		gen_mutated_children.append([])
		#generate popsize-k children
		while(x2 < (popsize - k)):
			indarr = np.random.choice(k, 2, replace = False, p=[0.3, 0.3, 0.15, 0.1, 0.1, 0.05])
			ind1 = indarr[0]
			ind2 = indarr[1]
			parent1 = np.copy(parents[ind1])
			parent2 = np.copy(parents[ind2])
			child1, child2 = crossover(parent1, parent2)
			gen_crossover_children[-1].append(child1)
			gen_crossover_children[-1].append(child2)
			child1 = mutate(child1, mut_prob, mut_range)
			child2 = mutate(child2, mut_prob, mut_range)
			gen_mutated_children[-1].append(child1)
			gen_mutated_children[-1].append(child2)

			#if any child is same as parent, discard the two children
			comparison1 = (child1 == parent1)
			comparison2 = (child2 == parent1)
			comparison3 = (child1 == parent2)
			comparison4 = (child2 == parent2)
			if(comparison1.all() == True or comparison2.all() == True or comparison3.all() == True or comparison4.all() == True):
				if comparison1 or comparison3:
					gen_crossover_children[-1].pop(-2)
					gen_mutated_children[-1].pop(-2)
				if comparison2 or comparison4:
					gen_crossover_children.pop()
					gen_mutated_children.pop()
				continue
			child_population[x2] = child1
			x2 += 1
			child_population[x2] = child2
			x2 += 1

		#find errors for children
		for i in range(popsize-k):
			child_err = client.get_errors(key, child_population[i].tolist())
			#for now, error=err[0]+err[1] but might change weightages later
			child_errors[i] = np.copy(child_err[0]+child_err[1]+factor*(abs(child_err[0]-child_err[1])))
			child_errors1[i] = np.copy(child_err[0])
			child_errors2[i] = np.copy(child_err[1])

		child_indices = np.zeros(popsize-k)
		temp_child_population = np.zeros((popsize-k, 11))
		temp_child_errors = np.zeros(popsize-k)
		temp_child_errors1 = np.zeros(popsize-k)
		temp_child_errors2 = np.zeros(popsize-k)

		#sort children
		child_indices = np.copy(np.argsort(child_errors))
		temp_child_population = np.copy(child_population)
		temp_child_errors = np.copy(child_errors)
		temp_child_errors1 = np.copy(child_errors1)
		temp_child_errors2 = np.copy(child_errors2)

		for i in range(popsize-k):
			child_population[i] = np.copy(temp_child_population[child_indices[i]])
			child_errors[i] = np.copy(temp_child_errors[child_indices[i]])
			child_errors1[i] = np.copy(temp_child_errors1[child_indices[i]])
			child_errors2[i] = np.copy(temp_child_errors2[child_indices[i]])

		new_population = np.zeros((popsize, 11))
		new_errors = np.zeros(popsize)
		new_errors1 = np.zeros(popsize)
		new_errors2 = np.zeros(popsize)
		#take all popsize-k children, and the top k parents
		for i in range(popsize-k):
			new_population[i] = np.copy(child_population[i])
			new_errors[i] = np.copy(child_errors[i])
			new_errors1[i] = np.copy(child_errors1[i])
			new_errors2[i] = np.copy(child_errors2[i])
		for i in range(k):
			new_population[popsize-k+i] = np.copy(population[i])
			new_errors[popsize-k+i] = np.copy(errors[i])
			new_errors1[popsize-k+i] = np.copy(errors1[i])
			new_errors2[popsize-k+i] = np.copy(errors2[i])

		population = np.copy(new_population)
		errors = np.copy(new_errors)
		errors1 = np.copy(new_errors1)
		errors2 = np.copy(new_errors2)
		indices = np.copy(np.argsort(errors))
		temp_population = np.copy(population)
		temp_errors = np.copy(errors)
		temp_errors1 = np.copy(errors1)
		temp_errors2 = np.copy(errors2)

		for i in range(popsize):
			population[i] = np.copy(temp_population[indices[i]])
			errors[i] = np.copy(temp_errors[indices[i]])
			errors1[i] = np.copy(temp_errors1[indices[i]])
			errors2[i] = np.copy(temp_errors2[indices[i]])


		print("Min error: ", errors1[0]+errors2[0])
		print("Train error: ", errors1[0])
		print("Val error: ", errors2[0])
		print("Diff: ", abs(errors1[0]-errors2[0]))
		print("\n")
		dict = {"population": population.tolist(), "top_train_error": errors1[0].tolist(), "top_val_error": errors2[0].tolist()}
		with open("dict55.json", "a") as f:
			json.dump(dict, f)


	final_vector = np.copy(population[0])
	return final_vector

ans = main()
generations()
#sub = client.submit(key, ans.tolist())
#print(sub)
