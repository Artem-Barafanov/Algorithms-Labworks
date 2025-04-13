#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>;
#include <sstream>
#include <string>
#include <vector>
#include <locale>
#include <random>

int GetRandomInt(int min, int max) {
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> dis(min, max);
	return dis(gen);
}

void GetVectorFromFile(const std::string& filename, std::vector<std::string>& names) {
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

int calc_K_anonimity(const std::string& filename) {
	std::ifstream file(filename);
	if (!file) {
		std::cerr << "Error opening file: " << filename << std::endl;
		return -1;
	}

	std::vector<std::string> lines;
	std::string line;
	while (getline(file, line)) {
		lines.push_back(line);
	}
	file.close();

	std::vector<std::vector<std::string>> attributes;
	for (const std::string& line : lines) {
		std::vector<std::string> attrs;
		std::string lineCopy = line;
		size_t pos = 0;
		while ((pos = lineCopy.find(';')) != std::string::npos) {
			attrs.push_back(lineCopy.substr(0, pos));
			lineCopy.erase(0, pos + 1);
		}
		attrs.push_back(lineCopy);
		attributes.push_back(attrs);
	}

	std::map<std::vector<std::string>, int> kAnonymity;
	for (const std::vector<std::string>& attrs : attributes) {
		kAnonymity[attrs]++;
	}
	std::vector<int> kValues;
	for (const auto& pair : kAnonymity) {
		kValues.push_back(pair.second);
	}
	sort(kValues.begin(), kValues.end());
	std::vector<double> kValues_in_per = {0,0,0,0,0};
	std::vector<std::string> unique_str;
	for (int i = 0; i < kValues.size(); ++i) {
		if (kValues[i] == 1 && filename == "depersonal.csv") {
			unique_str.push_back(lines[i]);
		}
		if (kValues[i] == kValues[0]) {
			kValues_in_per[0] += kValues[i];
		}
		if (kValues[i] == kValues[1]) {
			kValues_in_per[1] += kValues[i];
		}
		if (kValues[i] == kValues[2]) {
			kValues_in_per[2] += kValues[i];
		}
		if (kValues[i] == kValues[3]) {
			kValues_in_per[3] += kValues[i];
		}
		if (kValues[i] == kValues[4]) {
			kValues_in_per[4] += kValues[i];
		}
	}
	for (int i = 0; i < 5; ++i) {
		kValues_in_per[i] = (kValues_in_per[i] / lines.size()) * 100;
	}
	kValues.resize(5);

	std::cout << "5 плохих значений k-anonymity файла " << filename << ":" << std::endl;
	for (int i = 0; i < 5; i++) {
		std::cout << "k = " << kValues[i] << "\t" << kValues_in_per[i] << " %" << std::endl;
	}
	if (lines.size() <= 51000) {
		std::cout << "Приемлемое значение K: K >= 10" << std::endl << std::endl;
	}
	else if (lines.size() <= 105000) {
		std::cout << "Приемлемое значение K: K >= 7" << std::endl << std::endl;
	}
	else {
		std::cout << "Приемлемое значение K: K >= 5" << std::endl << std::endl;
	}
	if (unique_str.size() != 0) {
		std::cout << "Уникальные устроки:" << std::endl;
		for (int i = 0; i < unique_str.size(); ++i) {
			std::cout << unique_str[i] << std::endl;
		}
	}
	return 0;
}

std::string extract_first_name(const std::string& fio) {
	size_t space_pos = fio.find(' ', fio.find(' ') + 1);
	if (space_pos != std::string::npos) {
		size_t first_space_pos = fio.find(' ');
		return fio.substr(first_space_pos + 1, space_pos - first_space_pos - 1);
	}
	return "";
}

std::string anon_fio(const std::string& fio, const std::vector<std::string>& vec_male_names) {
	std::string first_name = extract_first_name(fio);
	for (int i = 0; i < vec_male_names.size(); ++i) {
		if (first_name == vec_male_names[i]) {
			return "М";
		}
	}
	return "Ж";
}

std::string anon_price(const std::string& price) {
	if (price[0] == '2' || price[0] == '3' || price[0] == '4' || price[0] == '5') {
		return "2000-6000";
	}
	else {
		return "6000-10000";
	}
}

std::string anon_an(const std::string& an) {
	int count = 0;
	for (int i = 0; i < an.size(); ++i) {
		if (an[i] == '/') {
			count++;
		}
	}
	if (count == 1) {
		return "Кол-во анализов: >1";
	}
	return "Кол-во анализов: 1";
}


std::string anon_symp(const std::string& symp,
	std::vector<std::string>& symp_intern_vector,
	std::vector<std::string>& symp_out_vector) {
	std::string str_return = "00";
	for (int i = 0; i < symp_intern_vector.size(); ++i) {
		if (symp == symp_intern_vector[i]) {
			str_return[0] = '1';
			break;
		}
	}
	for (int i = 0; i < symp_out_vector.size(); ++i) {
		if (symp == symp_out_vector[i]) {
			str_return[1] = '1';
			break;
		}
	}
	if (str_return[0] == '1' && str_return[1] == '0') {
		return "Внешние признаки";
	}
	else if (str_return[0] == '0' && str_return[1] == '1') {
		return "Боль во внутренних органах";
	}
	else {
		int x = GetRandomInt(1, 10);
		if (x <= 5) {
			return "Внешние признаки";
		}
		else {
			return "Боль во внутренних органах";
		}
	}
}

std::string anon_doctor(const std::string& doctor,
	std::vector<std::string>& doctors_vector,
	std::vector<int>& intern, std::vector<int>& surg,
	std::vector<int>& diag) {
	int i = 0;
	while (doctor != doctors_vector[i]) {
		i++;
	}
	if (std::find(intern.begin(), intern.end(), i) != intern.end()) {
		return "Внутренняя медицина и смежные специальности";
	}
	else if (std::find(surg.begin(), surg.end(), i) != surg.end()) {
		return "Хирургические и интервенционные специальности";
	}
	else {
		return "Специализация в области диагностики, профилактики и оказания вспомогательной помощи";
	}
}

std::string anon_card(const std::string& card) {
	if (card[1] == '4') {
		return "VISA/Альфа Банк";
	}

	else if (card[1] == '5') {
		return "MasterCard/Сбер Банк";
	}
	else {
		return "МИР/Т Банк";
	}
}
std::string anon_pass(const std::string& pass) {
	std::string mask = "Российский паспорт";
	return mask;
}

std::string anon_snils(const std::string& snils) {
	return "XXX-XXX-XXX XX";
}

std::string anon_date(const std::string& date) {
	int year = std::stoi(date.substr(0, 4));
	int month = std::stoi(date.substr(5, 2));
	int day = std::stoi(date.substr(8, 2));
	int hour = std::stoi(date.substr(11, 2));
	std::string shifr_date;

	shifr_date += "2015-2024/";

	if ((month >= 3 && month <= 5) || (month >= 9 && month <= 11)) {
		shifr_date += "Весна|Осень";
	}
	else {
		shifr_date += "Зима|Лето";
	}
	return shifr_date;
}

std::string anon_date_an(const std::string& date, const std::string& date_an) {
	int day_visit = std::stoi(date.substr(8, 2));
	int day_res = std::stoi(date_an.substr(8, 2));
	if (day_visit == day_res) {
		return "В тот же день";
	}
	else if (day_visit == day_res - 1) {
		return "Через день";
	}
	else {
		return "Через 2-3 дня";
	}
}

int main() {
	std::setlocale(LC_ALL, "Russian");
	std::ifstream file("outout.csv");
	std::ofstream fout("depersonal.csv");
	std::vector<std::string> doctors_vector;
	GetVectorFromFile("doctors.txt", doctors_vector);
	std::vector<std::string> symp_intern_vector;
	GetVectorFromFile("symp_intern.txt", symp_intern_vector);
	std::vector<std::string> symp_out_vector;
	GetVectorFromFile("symp_out.txt", symp_out_vector);
	std::vector<std::string> vec_male_names;
	GetVectorFromFile("male_names.txt", vec_male_names);
	std::vector<int> intern = { 0,1,2,3,4,6,7,8,9,10,12,14,18,19,34,38,40,44,46,49,50,53,55,56,57,61,76,81,83,84};
	std::vector<int> surg = { 13,29,30,35,36,41,45,47,48,52,54,58,60,62,63,68,69,70,71,73,74,75,77,78,79,82};
	std::vector<int> diag = { 5,11,15,16,17,20,21,22,23,24,25,26,27,28,31,32,33,37,39,42,43,51,59,64,65,66,67,72,80};
	
	std::cout << "Выберите квази-идентификаторы: \n Введите 1, если хотите выставить квази-идентификатор и 0 - в противном случае" << std::endl << std::endl;

	std::string line;
	std::string fio, pass, snils, symp, doctor, date, an, date_an, price, card;
	int kv_symp, kv_doctor, kv_date, kv_an, kv_date_an, kv_price, kv_card;
	std::cout << "Симптомы: ";
	std::cin >> kv_symp;
	std::cout << "Врач: ";
	std::cin >> kv_doctor;
	std::cout << "Дата посещения: ";
	std::cin >> kv_date;
	std::cout << "Анализы: ";
	std::cin >> kv_an;
	std::cout << "Дата получения анализов: ";
	std::cin >> kv_date_an;
	std::cout << "Стоимость: ";
	std::cin >> kv_price;
	std::cout << "Банковская карта: ";
	std::cin >> kv_card;
	std::cout << std::endl << std::endl << "Обезличивание и подсчет K-anonymity:" << std::endl;
	while (std::getline(file, line)) {
		std::stringstream ss(line);
		std::getline(ss, fio, ';');
		std::getline(ss, pass, ';');
		std::getline(ss, snils, ';');
		std::getline(ss, symp, ';');
		std::getline(ss, doctor, ';');
		std::getline(ss, date, ';');
		std::getline(ss, an, ';');
		std::getline(ss, date_an, ';');
		std::getline(ss, price, ';');
		std::getline(ss, card);

		fout << anon_fio(fio, vec_male_names) << ";";
		fout << anon_pass(pass) << ";";
		fout << anon_snils(snils) << ";";
		if (kv_symp == 1) {
			fout << anon_symp(symp, symp_intern_vector, symp_out_vector) << ";";
		}
		else {
			fout << symp << ";";
		}
		if (kv_doctor == 1) {
			fout << anon_doctor(doctor, doctors_vector, intern, surg, diag) << ";";
		}
		else {
			fout << doctor << ";";
		}
		if (kv_date == 1) {
			fout << anon_date(date) << ";";
		}
		else {
			fout << date << ";";
		}
		if (kv_an == 1) {
			fout << anon_an(an) << ";";
		}
		else {
			fout << an << ";";
		}
		if (kv_date_an == 1) {
			fout << anon_date_an(date, date_an) << ";";
		}
		else {
			fout << date_an << ";";
		}
		if (kv_price == 1) {
			fout << anon_price(price) << ";";
		}
		else {
			fout << price << ";";
		}
		if (kv_card == 1) {
			fout << anon_card(card) << std::endl;
		}
		else {
			fout << card << std::endl;
		}
	}
	calc_K_anonimity("outout.csv");
	calc_K_anonimity("depersonal.csv");
	fout.close();
	file.close();
}