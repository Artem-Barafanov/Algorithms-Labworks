#include "Person.h"
#include <locale>

int GetRandomInt(int min, int max) {
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> dis(min, max);
	return dis(gen);
}

void GetVectorFromFile(const std::string& filename, std::vector<std::string> &names) {
	std::ifstream file(filename);
	if (!file) {
		std::cout << "Error";
	}
	std::string line;
		while (std::getline(file, line)) {
			names.push_back(line);
		}
	file.close();
}

int main() {
	std::setlocale(LC_ALL, "Russian");
	int number_of_lines;
	std::cout << "Введите количество строк в датасете (min 50000)" << std::endl;
	std::cin >> number_of_lines;
	int x1, x2;
	std::cout << "Введите вероятность отплаты картами систем Visa и Mastervard (два числа)" << std::endl;
	std::cin >> x1 >> x2;
	if (x1 + x2 > 100 || number_of_lines<50000) {
		std::cout << "Ошибка! Некорректные данные";
		return 0;
	}
	std::cout << "Генерация датасета..." << std::endl;
	std::vector<std::string> male_names_vector;
	std::vector<std::string> male_surnames_vector;
	std::vector<std::string> male_midnames_vector;
	std::vector<std::string> female_names_vector;
	std::vector<std::string> female_surnames_vector;
	std::vector<std::string> female_midnames_vector;

	std::vector<std::string> symptoms_vector;

	std::vector<std::string> doctors_vector;

	std::vector<std::string> analyzes_vector;

	GetVectorFromFile("male_names.txt", male_names_vector);
	GetVectorFromFile("female_names.txt", female_names_vector);
	GetVectorFromFile("male_surnames.txt", male_surnames_vector);
	GetVectorFromFile("female_surnames.txt", female_surnames_vector);
	GetVectorFromFile("male_midnames.txt", male_midnames_vector);
	GetVectorFromFile("female_midnames.txt", female_midnames_vector);

	GetVectorFromFile("symptoms.txt", symptoms_vector);

	GetVectorFromFile("doctors.txt", doctors_vector);

	GetVectorFromFile("analyzes.txt", analyzes_vector);

	std::vector<Person> clinic;
	Person a;
	std::ofstream fout("outout.csv");
	for (int i = 0; i < number_of_lines; ++i) {
		int x = GetRandomInt(1,3);
		if (x != 3 || clinic.size()<2) {
			a.Generate_Person(male_names_vector,
						male_surnames_vector,
						male_midnames_vector,
						female_names_vector,
						female_surnames_vector,
						female_midnames_vector,
						symptoms_vector,
						doctors_vector,
						analyzes_vector,
						x1, x2);
			a.PrintPerson(fout);
			clinic.push_back(a);
		}
		else {
			int number = GetRandomInt(0, clinic.size() - 1);
			a.Repeat_Person(clinic, number, symptoms_vector,
							doctors_vector,
							analyzes_vector, x1, x2);
			clinic[number].PrintPerson(fout);
		}
	}
	fout.close();
}