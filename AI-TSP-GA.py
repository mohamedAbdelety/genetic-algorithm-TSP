import random
from random import randrange
from time import time


class Problem_Genetic(object):
    # =====================================================================================================================================
    # Class to represent problems to be solved by means of a general
    # genetic algorithm. It includes the following attributes:
    # - genes: list of possible genes in a chromosome
    # - individuals_length: length of each chromosome
    # - decode: method that receives the genotype (chromosome) as input and returns
    #    the phenotype (solution to the original problem represented by the chromosome)
    # - fitness: method that returns the evaluation of a chromosome (acts over the
    #    genotype)
    # - mutation: function that implements a mutation over a chromosome
    # - crossover: function that implements the crossover operator over two chromosomes
    # =====================================================================================================================================

    def __init__(self, genes, individuals_length, decode, fitness):
        self.genes = genes
        self.individuals_length = individuals_length
        self.decode = decode
        self.fitness = fitness


    # المسولة عن الطفرة خدت الكرموسوم وخدت النسبة
    def mutation(self, chromosome, prob):

        def inversion_mutation(chromosome_aux):
            chromosome = chromosome_aux
            index1 = randrange(0, len(chromosome)) # start index
            index2 = randrange(index1, len(chromosome)) # end index
            chromosome_mid = chromosome[index1:index2] # الحتة من الكرموسوم اللى هعمله طفره عن طريق انى اعكس الجين
            chromosome_mid.reverse()
            chromosome_result = chromosome[0:index1] + chromosome_mid + chromosome[index2:] # الكرسموم بعد الطفرة الحتة الاول زى مهى و الاخيرة والحتة اللى فى النص بعد معكسته

            return chromosome_result

        aux = []
        for _ in range(len(chromosome)): # هنا بتلف على الكرموسوم وتجيب رقم عشوائى لو طلع اقل من النسبة يبقى هعمل طفرة
            if random.random() < prob: # بترجع من 0 الى 1
                aux = inversion_mutation(chromosome)# هنا كدة اه انا هعمل طفرة والكرموسوم هيرجعلى بعد معملتله طفرة
        return aux







    # بتاخد 2 كرموسوم تجوزهم وترجع اطفالهم
    def crossover(self, parent1, parent2):
        # دلوقتى طلعت كرموسوم الطفل بس عايز اشوف هل فى الطفل ده جينات متكررة ولا لا
        def process_gen_repeated(copy_child1, copy_child2):
            # الجزء الاول يشتغل على الطفل الاول
            # هيعمل ايه ؟!!
            # هيشوف فى تكرار ولا لا بالنسبة لاول جزء لو لقى فى تكرار هو واخد اول جزء من اول اب فهيروح يشيل واحدة من المتكررين ويحد جين بداله من الاب بس يبقى مش موجود فى الابن
            count1 = 0
            for gen1 in copy_child1[:pos]:
                repeat = 0
                repeat = copy_child1.count(gen1)
                if repeat > 1:  # If need to fix repeated gen
                    count2 = 0
                    for gen2 in parent1[pos:]:  # Choose next available gen
                        if gen2 not in copy_child1:
                            child1[count1] = parent1[pos:][count2]
                        count2 += 1
                count1 += 1
            # الجزء التانى يشتغل على الطفل التانى
            count1 = 0
            for gen1 in copy_child2[:pos]:
                repeat = 0
                repeat = copy_child2.count(gen1)
                if repeat > 1:  # If need to fix repeated gen
                    count2 = 0
                    for gen2 in parent2[pos:]:  # Choose next available gen
                        if gen2 not in copy_child2:
                            child2[count1] = parent2[pos:][count2]
                        count2 += 1
                count1 += 1

            return [child1, child2]




        # سهلين مفهمش حاجة عمل الطفلين وبعتهم للفنكشن اللى فوق
        pos = random.randrange(1, self.individuals_length - 1)
        child1 = parent1[:pos] + parent2[pos:]
        child2 = parent2[:pos] + parent1[pos:]

        return process_gen_repeated(child1, child2)# هيرجع الطفلين من غير تكرار فى جيناتهم














# مش محتجة تديله الكرموسوم بدل ممكتوب كدة [1,3,4,0,7,5,2,6]
# يحوله للشكل النهائى [B,D,E,A,H,F,C,G]
def decodeTSP(chromosome):
    lista = []
    for i in chromosome:
        lista.append(cities.get(i))
    return lista



# دى فنكشن بتفرض عقاب لو لقت ان جوة الكرموسوم جينات متكررة
# والعقاب بيزيد كل متلاقى جينات اكتر متكررة وبترجع مقدار العقاب بتاعه
def penalty(chromosome):
    actual = chromosome
    value_penalty = 0
    for i in actual:
        times = 0
        times = actual.count(i)
        if times > 1:
            value_penalty += 100 * abs(times - len(actual))
    return value_penalty



# دى الفنكشن اللى بتحسب ال fitness لكل كرموسوم
# عشان انا هناك بختار الاقل قيمة عشان ميحصلش ليه تزاوج
# القيمة بتحسبها ازاى بتروح على اول جين (مدينة)وتجيب المسافة بينها وبين المدينة اللى بعدها فى الكرموسوم وتجمع عليه قيمة العقاب
# لما توصل لاخر جين انا عايز ارجع للاول خالص لاول جين لاول مدينة عشان اجيب المسافة بينهم
def fitnessTSP(chromosome):
    def distanceTrip(index, city): # بتجيب المسافات من الجراف اللى فى الاول
        w = distances.get(index)
        return w[city]

    actualChromosome = list(chromosome)
    fitness_value = 0
    count = 0

    # Penalty for a city repetition inside the chromosome
    penalty_value = penalty(actualChromosome)

    for i in chromosome:
        if count == 7: # اخر جين جوة الكرموسوم
            nextCity = actualChromosome[0]
        else:
            temp = count + 1
            nextCity = actualChromosome[temp]

        fitness_value += distanceTrip(i, nextCity) + 50 * penalty_value
        count += 1

    return fitness_value # فى الاخر خالص هجيب القيمة الكلية للكرموسوم كامل اللى هى مجموع المسافات بين المدن بالاضافة لل penalty






# ========================================================== FIRST PART: GENETIC OPERATORS============================================
# Here We defined the requierements functions that the GA needs to work
# The function receives as input:
# * problem_genetic: an instance of the class Problem_Genetic, with
#     the optimization problem that we want to solve.
# * k: number of participants on the selection tournaments.
# * opt: max or min, indicating if it is a maximization or a
#     minimization problem.
# * ngen: number of generations
# * size: number of individuals for each generation
# * ratio_cross: portion of the population which will be obtained by
#     means of crossovers.
# * prob_mutate: probability that a gene mutation will take place.
# =====================================================================================================================================


def genetic_algorithm_t(Problem_Genetic, k, opt, ngen, size, ratio_cross, prob_mutate):
    #one population conatain list of 100 list // 100 is size every 1 from 100 is cromosom have random gene
    #output 100 chromosom
    #population سكان الجيل
    def initial_population(Problem_Genetic, size):
        def generate_chromosome():
            chromosome = Problem_Genetic.genes[:]
            random.shuffle(chromosome)
            return chromosome

        return [generate_chromosome() for _ in range(size)]





    # دى المسولة انها تكون الجيل الجديد اللى هو هيكون 100 برده
    # هتكون الجيل الجديد وترجعه عشان هو كمان يرجع هنا يتعمله نفس الكلام
    # الفنكشن دى هتتعمل 200 مرة لانها محطوطة فى loop
    # يعنى هفضل امشى ل 200 جيل للامام فهوصل لجيل جامد جدى !!
    def new_generation_t(Problem_Genetic, k, opt, population, n_parents, n_directs, prob_mutate):
        # دى الفنكشن اللى هتختار مين ال 20 اللى مش هيتجوزوا
        def tournament_selection(Problem_Genetic, population, n, k, opt):
            winners = [] # دى القائمة اللى انا مختارهم احسن 20 كرموسوم عشان انا مش محتاج اجوزهم هم كدة تمام خواصهم حلوة
            # طيب هنا هختار زى احسن 20 (زى)عن طريق ال fitness
            for _ in range(n): # n = 20
                elements = random.sample(population, k) # هاخد من السكان اللى هم ال 100 هاخد عدد k =2 كل مرة
                #  واجى على ال 2 واختار اللى اقل fitness واضيفه فى اللى مش هيتجوزوا
                winners.append(opt(elements, key=Problem_Genetic.fitness))
            return winners


        #  بتاخد قائمة بالكرموسومات اللى هتتجوز وترجع الاطفال نتيجة التزاوج
        def cross_parents(Problem_Genetic, parents):
            childs = []
            for i in range(0, len(parents), 2): # هاخد كل 2 ورا بعض ابعتهم للفنكشن اللى هتجوزهم والناتج بتاع التزاوج هضيفه لقائمة الاطفال
                childs.extend(Problem_Genetic.crossover(parents[i], parents[i + 1]))
            return childs


        def mutate(Problem_Genetic, population, prob):
            # لاحظ هنا ال popualtion هم الاطفال الناتجين من التزاوج عشان دول اللى بيتعملهم طفرة
            for i in population:
                Problem_Genetic.mutation(i, prob)
            return population # هترجع ال 80 بعد التغيير بع الطفرة اللى هى نسبتها قليلة




        # لاحظ اننا هناك قلت هعمل تزاوج ل 80 وهسيب 20 من غير تزاوج لكن محددتش مين من الجيل هيتجوز ومين لا
        directs = tournament_selection(Problem_Genetic, population, n_directs, k, opt)#k=2
        # دى بقى هتكون list of 20 list واللى هيكون فيهم ال 20 اللى مش هيتجوزوا هيختارهم عن طريف الفنكشن اللى فوق
        crosses = cross_parents(Problem_Genetic, tournament_selection(Problem_Genetic, population, n_parents, k, opt))
        # هنا بقى هعمل الفنكشن اللى مسولة عن ال 80 اللى هيتجوزوا وبعتلها الفنكشن اللى بتختار ال 80 اللى هيتجوزوا وهروح اعمل التزاوج
        # هترجع ال 80 طفل ناتجين عن عملية التزاوج


        # بعد معملت الحاجات اللى هتتجوز وجبت اطفالهم والحاجات اللى مش هتتجوز هعمل بقى الطفرة اللى بتكون فى بعض الكرموسومات الاطفال اللى ناتجين من التزاوج
        mutations = mutate(Problem_Genetic, crosses, prob_mutate)

        # الجيل الجديد هيكون ال 20 اللى متجوزش وال 80 طفل الناتجين من التزاوج بعد معملت ليهم طفرة
        new_generation = directs + mutations

        return new_generation # الجيل الجديد بعد التزاوج والطفرة







    population = initial_population(Problem_Genetic, size)# ده بيكون اول جيل اللى هبدا من عنده انى اعمل باقى الاجيال
    n_parents = round(size * ratio_cross) # مين من 100 اللى هم عدد الكرموسومات فى الجيل الواحد (population)هيتعملهم تزاوج
    if n_parents % 2 == 1:
        n_parents -= 1
    n_directs = size - n_parents # دول بقى اللى مش هجوزهم وهيفضلوا زى مهم لاحظ ان كل جيل عدد ال population بتاعه متساوى

    for _ in range(ngen):#N generation = 200 يعنى هعمل 200جيل
        # كل جيل عدد سكانه 100 زى مقلنا فوق
        population = new_generation_t(Problem_Genetic, k, opt, population, n_parents, n_directs, prob_mutate)
        # هنا دى زى recursion خدنا هنا فى الاول اول جيل اللى هو متخزن هنا اللى هو list of 100 list
        # وبعتناه لفنكشن عشان تجيب الجيل التالى من ده ادناه مين اللى هيجوزوه ومين لا ونسبة الطفرة اللى هتحصل
        # k=2
        # وكل جيل ياخد ويعمله عليه لحد ما اخر جيل هو اللى هيكون معاى فى ال population اللى هو الجيل ال 200 احفاد الاحفاد الاحفاد ههههههههه!!
    bestChromosome = opt(population, key=Problem_Genetic.fitness)
    # هنا بقى هجيب اخر جيل اللى فيه 100 كرموسوم واشوف احسنهم اقلهم مسافة وده اللى هيطبع
    # لاحظ بعمل كل الكلام ده 10 مرات مختلفة ب 10 حلول مختلفة
    print("Chromosome: ", bestChromosome)
    # هعمل decode عشان اجيب الاسماء الحقيقية
    genotype = Problem_Genetic.decode(bestChromosome)
    print("Solution:", (genotype, Problem_Genetic.fitness(bestChromosome)))
    return (genotype, Problem_Genetic.fitness(bestChromosome))


# ============================================================ SECOND PART: VARIANTS OVER THE STANDARD GENETIC ALGORITHM =========================================
# Modify the standard version of genetic algorithms developed in the previous step, by choosing only one of the following:
# Genetic Algorithm with Varying Population Size
#
# *** -> We choose this option
#
# The idea is to introduce the concept of "ageing" into the population of chromosomes.
# Each individual will get a "life-expectancy" value, which directly depends on the fitness. Parents are selected randomly,
# without paying attention to their fitness, but at each step all chromosomes gain +1 to their age,
# and those reaching their life-expectancy are removed from the population.
# It is very important to design a good function calculating life-expectancy, so that better individuals survive during more generations,
# and therefore get more chances to be selected for crossover.
#
# Cellular Genetic Algorithm
# The idea is to introduce the concept of "neighbourhood" into the population of chromosomes (for instance, placing them into
# a grid-like arrangement),
# in such a way that each individual can only perform crossover with its direct neighbours.
# =====================================================================================================================================


# لاحظ انا عايز افهم ايه الحكمة من ال dictionary الفاضى ده
def genetic_algorithm_t2(Problem_Genetic, k, opt, ngen, size, ratio_cross, prob_mutate, dictionary):
    # اختلاف بسيط اوى هنا
    def initial_population(Problem_Genetic, size):

        def generate_chromosome():
            chromosome = []
            chromosome = Problem_Genetic.genes[:]
            random.shuffle(chromosome)
            # Adding to dictionary new generation الجديد هنا
            dictionary[str(chromosome)] = 1 # dictionary['02146357']=1
            # لاحظ هنا انا يعتبر انا ضفت كل الكرموسومات اللى عملته فى ال dictionary بس من خواص الدكشنرى انه مفهوش تكرار فكدة ضمنت ان مفيش كرموسومات هتتكرر فين؟ فى الدكشنرى
            return chromosome

        return [generate_chromosome() for _ in range(size)]

    # عايز بقى اكون الجيل الجديد
    def new_generation_t(Problem_Genetic, k, opt, population, n_parents, n_directs, prob_mutate):
        # جزء جديد بسيط ان اللى هعملهم انهم ميتجوزوش هزود قيمتهم واحد بس كدة
        def tournament_selection(Problem_Genetic, population, n, k, opt):
            winners = []
            for _ in range(int(n)):
                elements = random.sample(population, k)
                winners.append(opt(elements, key=Problem_Genetic.fitness))
            # الجديد هنا (عندى ملحوظة هنا)مهو كدة كدة اكيد موجود فى الدكشنرى
            for winner in winners:
                # For each winner, if exists in dictionary, we increase his age
                if str(winner) in dictionary:
                    dictionary[str(winner)] = dictionary[str(winner)] + 1
                # Else we need to initializate in dictionary شايفه ملهاش لازمة
                else:
                    dictionary[str(winner)] = 1
            return winners


        def cross_parents(Problem_Genetic, parents):
            childs = []
            for i in range(0, len(parents), 2):
                childs.extend(Problem_Genetic.crossover(parents[i], parents[i + 1]))
                # Each time that some parent are crossed we add their two sons to dictionary الجديد
                if str(parents[i]) not in dictionary:
                    dictionary[str(parents[i])] = 1
                # هحط فى الدكشنرى الابن واديله قيمة الاب وبعد كدة احذف الاب
                dictionary[str(childs[i])] = dictionary[str(parents[i])]
                # ...and remove their parents
                del dictionary[str(parents[i])]

            return childs


        def mutate(Problem_Genetic, population, prob):
            j = 0
            copy_population = population
            for cross_m in population:
                Problem_Genetic.mutation(cross_m, prob)
                # Each time that some parent is crossed الجديد
                if str(cross_m) in dictionary:
                    # We add the new chromosome mutated
                    # هنزود الكرموسوم بعد التعديل وهحذف القديم
                    dictionary[str(population[j])] = dictionary[str(cross_m)]
                    # Then we remove the parent, because his mutated has been added.
                    del dictionary[str(copy_population[j])]# انا شايف ان دى ملهاش لازمة
                    j += 1
            return population


        # كاستدعاء فنكسن وبرامتر بتاع كل فنكشن زى مهو
        directs = tournament_selection(Problem_Genetic, population, n_directs, k, opt)
        crosses = cross_parents(Problem_Genetic, tournament_selection(Problem_Genetic, population, n_parents, k, opt))
        mutations = mutate(Problem_Genetic, crosses, prob_mutate)
        new_generation = directs + mutations

        # Adding new generation of mutants to dictionary.
        for i in new_generation:
            age = 0
            if str(i) in dictionary:
                age += 1
                dictionary[str(i)] += 1
            else:
                dictionary[str(i)] = 1
        return new_generation






    population = initial_population(Problem_Genetic, size)
    n_parents = round(size * ratio_cross)
    if n_parents % 2 == 1:
        n_parents -= 1
    n_directs = size - n_parents

    for _ in range(ngen):# هروح هنا عشان اعمل الاجيال الجديدة بعد معملت ال inital generation
        population = new_generation_t(Problem_Genetic, k, opt, population, n_parents, n_directs, prob_mutate)

    bestChromosome = opt(population, key=Problem_Genetic.fitness)
    print("Chromosome: ", bestChromosome)
    genotype = Problem_Genetic.decode(bestChromosome)
    print("Solution:", (genotype, Problem_Genetic.fitness(bestChromosome)), dictionary[(str(bestChromosome))],
          " generations of winners parents.")

    return (genotype, Problem_Genetic.fitness(bestChromosome)
            + dictionary[(str(bestChromosome))] * 50)  # Updating fitness with age too









# ========================================================================THIRD PART: EXPERIMENTATION=========================================================
# Run over the same instances both the standard GA (from first part) as well as the modified version (from second part).
# Compare the quality of their results and their performance. Due to the inherent randomness of GA,
# the experiments performed over each instance should be run several times.
# ============================================================================================================================================================


def TSP(k):
    # from me Problem_Genetic response crossover, mutation functions
    TSP_PROBLEM = Problem_Genetic([0, 1, 2, 3, 4, 5, 6, 7], len(cities), lambda x: decodeTSP(x),
                                  lambda y: fitnessTSP(y))
    #lambda x: decodeTSP(x),lambda y: fitnessTSP(y) x,y here is chromsom
    def first_part_GA(k):

      cont = 0
        print(
            "---------------------------------------------------------Executing FIRST PART: TSP --------------------------------------------------------- \n")
        time_initial_t2 = time()
        while cont <= k:
            genetic_algorithm_t(TSP_PROBLEM, 2, min, 200, 100, 0.8, 0.05)
            cont += 1
        time_final_t2 = time()
        print("")
        print("Total time: ", (time_final_t2 - time_initial_t2), " secs.\n")


    # part two بقى
    def second_part_GA(k):
        print(
            "---------------------------------------------------------Executing SECOND PART: TSP --------------------------------------------------------- \n")
        cont = 0
        time_initial_t2 = time()
        while cont <= k:
            genetic_algorithm_t2(TSP_PROBLEM, 2, min, 200, 100, 0.8, 0.05, {}) # ده الزيادة ال dictionary اللى فى الاخر
            cont += 1
        time_final_t2 = time()
        print("")
        print("Total time: ", (time_final_t2 - time_initial_t2), " secs.\n")



    first_part_GA(k)
    print(
        "------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    second_part_GA(k)

















# ---------------------------------------- AUXILIARY DATA FOR TESTING --------------------------------


cities = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}

# Distance between each pair of cities

w0 = [999, 454, 317, 165, 528, 222, 223, 410]
w1 = [453, 999, 253, 291, 210, 325, 234, 121]
w2 = [317, 252, 999, 202, 226, 108, 158, 140]
w3 = [165, 292, 201, 999, 344, 94, 124, 248]
w4 = [508, 210, 235, 346, 999, 336, 303, 94]
w5 = [222, 325, 116, 93, 340, 999, 182, 247]
w6 = [223, 235, 158, 125, 302, 185, 999, 206]
w7 = [410, 121, 141, 248, 93, 242, 199, 999]

distances = {0: w0, 1: w1, 2: w2, 3: w3, 4: w4, 5: w5, 6: w6, 7: w7}

if __name__ == "__main__":
    # Constant that is an instance object
    genetic_problem_instances = 10
    print("EXECUTING ", genetic_problem_instances, " INSTANCES \n")
    TSP(genetic_problem_instances)
