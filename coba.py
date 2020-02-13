import random
import copy
import matplotlib.pyplot as plt

class kromosom:
    def __init__(self, n=1, individu = []) :
        pekerja = 13
        if n == 1 :
            individu = []
            for i in range(30):
                harian  = []
                for j in range(3):
                    harian.append(random.sample(range(1,pekerja+1),3))
                individu += [harian]
        self.individu = individu
        self.fitness = -1
    
gene = []
pop = []
offspring = []
population = 100

def fitness(pop):
    for individu in pop:
        n = individu.individu
        penalty = count_penalty(n)
        individu.fitness = 100/(100+penalty)

    

def count_penalty(individu):
    penalty = 0
    libur = [[1,2,3,4,5,6,7,8,9,10,11,12,13],[0,0,0,0,0,0,0,0,0,0,0,0,0]]
    #1 Hari 2x kerja dan hitung hari libur
    for day in range(len(individu)):
        seen = set()
        for shift in range(len(individu[day])):
            for i in range (len(individu[day][shift])):
                if individu[day][shift][i] in seen :
                    penalty = penalty + 1
                else :
                    seen.add(individu[day][shift][i])
        for j in range (13):
            if libur[0][j] not in seen :
                libur[1][j-1] = libur[1][j-1]+1
                
    for i in range(13):
        if libur[1][i] > 8 :
            penalty = penalty + (libur[1][i] - 8)                
    
    #shift malam tidak boleh dilanjut shift pagi
    for day in range(len(individu)-1):
        seen = set()
        for i in range(len(individu[day][2])):
            seen.add(individu[day][2][i])
        for j in range(len(individu[day][1])):
            if individu[day+1][0][j] in seen :
                penalty = penalty +1
    return penalty

def selection(pop):

    pop = sorted(pop, key=lambda individu: individu.fitness, reverse=True)
    pop = pop[:100]
    
    return pop


def mutasi(gene, mutation_rate):
#    mutation_rate = 0.6
    for individu in gene :
        tes = copy.deepcopy(individu)
        if random.random() < mutation_rate :
            tempa = [random.randint(0,29),random.randint(0,2),random.randint(0,2)] 
            tempb = [random.randint(0,29),random.randint(0,2),random.randint(0,2)] 
            temp = tes[tempa[0]][tempa[1]][tempa[2]]
            tes[tempa[0]][tempa[1]][tempa[2]] = tes[tempb[0]][tempb[1]][tempb[2]]
            tes[tempb[0]][tempb[1]][tempb[2]] = temp
            offspring.append(tes)
#        pop.append(kromosom(0, offspring))
#        gene.append(offspring)


def crossover(gene, crossover_rate):
#    crossover_rate = 0.4
    for i in range(len(gene)//2) :
        if random.random() < crossover_rate :
            parent1 = random.choice(gene)
            parent2 = random.choice(gene)
            child1 = copy.deepcopy(parent1)
            child2 = copy.deepcopy(parent2)
            split1 = random.randint(0,29)
            split2 = random.randint(0,2)
            split3 = random.randint(0,2)
            child1 = parent1[0:split1] + [parent1[split1][0:split2] + [parent1[split1][split2][0:split3]+parent2[split1][split2][split3:3]] + parent2[split1][split2+1:3]] + parent2[split1+1:30]
            child2 = parent2[0:split1] + [parent2[split1][0:split2] + [parent2[split1][split2][0:split3]+parent1[split1][split2][split3:3]] + parent1[split1][split2+1:3]] + parent1[split1+1:30]
            offspring.append(child1)
            offspring.append(child2)

        
def combine(offspring) :
    for i in range(len(offspring)):
        pop.append(kromosom(0,offspring[i]))

def count_avg(pop):
    total = 0
    for i in range(len(pop)):
        total += pop[i].fitness
    
    return total/len(pop)


def generate_individu(n):
    
    for i in range(n) :
        pop.append(kromosom())
        
    return pop
    
def init():
    gene.clear()
    offspring.clear()
    
    for i in range(0,len(pop)):
        gene.append(pop[i].individu)
            
            
def main(n):
    global pop
    y = []
    y1 = []
    x = []
    mutation_rate = 0.4
    crossover_rate = 0.6
    for i in range(n):
        print('Generasi : ' + str(i+1))
        init()
        mutasi(gene, mutation_rate)
        crossover(gene, crossover_rate)
        combine(offspring)
        fitness(pop)
        pop = selection(pop)
        favg = count_avg(pop)
        print('Fitness Terbaik : '+ str(pop[0].fitness))
        print('Rata-rata Fitness : '+ str(favg))
        y += [pop[0].fitness]
        y1 += [favg]
    
    for j in range(n):
        x += [j+1]
        
    plt.plot(x, y, label = "Fitness Tertinggi")
    plt.plot(x, y1, linestyle='dashed', label = "Rata-rata")
  
    plt.xlabel('Generasi') 
    plt.ylabel('Fitness')
    plt.legend(loc='best')
    plt.show()
