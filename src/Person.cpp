#include "Person.h"

int Person::id_generate = 10000;

void Person::SetId() {
	this->id = std::to_string(id_generate);
}

void Person::Generate_fio(const std::vector<std::string> &male_names, const std::vector<std::string>& female_names,
							const std::vector<std::string>& male_surnames, const std::vector<std::string>& female_surnames,
							const std::vector<std::string>& male_midnames, const std::vector<std::string>& female_midnames) {
	int pol = GetRandomInt(1, 2);
	std::string name;
	std::string surname;
	std::string midname;
	if (pol == 1) {
		name = male_names[GetRandomInt(0, male_names.size()-1)];
		surname = male_surnames[GetRandomInt(0, male_surnames.size()-1)];
		midname = male_midnames[GetRandomInt(0, male_midnames.size()-1)];
	}
	else {
		name = female_names[GetRandomInt(0, female_names.size()-1)];
		surname = female_surnames[GetRandomInt(0, female_surnames.size()-1)];
		midname = female_midnames[GetRandomInt(0, female_midnames.size()-1)];
	}
	this->fio = surname + ' ' + name + ' ' + midname;
}

void Person::Generate_passport() {
	std::string p = std::to_string(GetRandomInt(10000, 99999));
	std::string p0(1, p[0]);
	std::string p1(1, p[1]);
	std::string p2(1, p[2]);
	std::string p3(1, p[3]);
	std::string p4(1, p[4]);
	std::string id0(1, id[0]);
	std::string id1(1, id[1]);
	std::string id2(1, id[2]);
	std::string id3(1, id[3]);
	std::string id4(1, id[4]);
	this->passport = p0 + id0 + p1 + id1 + "  " + p2 + id2 + p3 + id3 + p4 + id4;
}

void Person::Generate_snils() {
	int i = 99999 - int(id_generate);
	std::string j = std::to_string(i);
	std::string p = std::to_string(GetRandomInt(100000, 999999));
	std::string p0(1, p[0]);
	std::string p1(1, p[1]);
	std::string p2(1, p[2]);
	std::string p3(1, p[3]);
	std::string p4(1, p[4]);
	std::string p5(1, p[5]);
	std::string j0(1, j[0]);
	std::string j1(1, j[1]);
	std::string j2(1, j[2]);
	std::string j3(1, j[3]);
	std::string j4(1, j[4]);
	this->snils = p0+j0+p1+'-'+j1+p2+j2+'-'+p3+j3+p4+' '+j4+p5;
	id_generate++;
}

void Person::Generate_doctor_symp_an(const std::vector<std::string>& doctors_vector,
									const std::vector<std::string>& symptoms_vector,
									const std::vector<std::string>& analyzes_vector) {
	int x = GetRandomInt(0, doctors_vector.size() - 1);
	this->doctor = doctors_vector[x];
	int y = GetRandomInt(x * 63, x * 63 + 62);
	this->symptoms = symptoms_vector[y];
	int z = GetRandomInt(x * 6, x * 6 + 5);
	this->analyzes = analyzes_vector[z];
}

void Person::Generate_date_vis_and_an() {
	do {
		timeStruct_vis.tm_year = GetRandomInt(2015, 2023) - 1900;
		timeStruct_vis.tm_mon = GetRandomInt(0, 11);
		timeStruct_vis.tm_mday = GetRandomInt(1, 31);
		timeStruct_vis.tm_hour = GetRandomInt(8, 18);
		timeStruct_vis.tm_min = GetRandomInt(0, 11)*5;
		mktime(&timeStruct_vis);
	} while (!(timeStruct_vis.tm_wday >= 1 && timeStruct_vis.tm_wday <= 5));
	do {
		timeStruct_an = timeStruct_vis;
		int wait = GetRandomInt(24, 72);
		int wait_min = GetRandomInt(0, 59);
		timeStruct_an.tm_sec += (wait * 3600 + wait_min * 60);
		mktime(&timeStruct_an);
	} while (!(timeStruct_an.tm_wday >= 1 && timeStruct_an.tm_wday <= 5) || (timeStruct_an.tm_hour<8) || 
				(timeStruct_an.tm_hour>18));
}

void Person::Generate_new_vis_and_an() {
	do {
		int wait = GetRandomInt(24, 8550);
		int wait_min = GetRandomInt(0, 59);
		timeStruct_vis.tm_sec += (wait * 3600 + wait_min * 60);
		mktime(&timeStruct_vis);
	} while (!(timeStruct_vis.tm_wday >= 1 && timeStruct_vis.tm_wday <= 5) || (timeStruct_vis.tm_hour < 8) ||
		(timeStruct_vis.tm_hour > 18));
	do {
		timeStruct_an = timeStruct_vis;
		int wait = GetRandomInt(24, 72);
		int wait_min = GetRandomInt(0, 59);
		timeStruct_an.tm_sec += (wait * 3600 + wait_min * 60);
		mktime(&timeStruct_an);
	} while (!(timeStruct_an.tm_wday >= 1 && timeStruct_an.tm_wday <= 5) || (timeStruct_an.tm_hour < 8) ||
		(timeStruct_an.tm_hour > 18));
}

void Person::Generate_price() {
	size_t pos = analyzes.find("/");
	if (pos != std::string::npos) {
		this->price = std::to_string(GetRandomInt(2000, 5000) + GetRandomInt(2000, 5000)) + " rub";
	}
	else {
		this->price = std::to_string(GetRandomInt(2000, 5000)) + " rub";
	}
}

void Person::Generate_card(int& x1, int& x2) {
	card = "";
	int syst = GetRandomInt(1, 100);
	if (syst >= 1 && syst <= x1) {
		card.push_back('4'); // Visa
		int bank = GetRandomInt(1, 100);
		if (bank >= 1 && bank <= 20) { card.insert(1, "960 14"); } // Альфа Банк
		if (bank > 20 && bank <= 40) { card.insert(1, "222 87"); } // Райффайзен Банк
		if (bank > 40 && bank <= 60) { card.insert(1, "274 32"); } // Сбер Банк
		if (bank > 60 && bank <= 80) { card.insert(1, "377 72"); } // Т Банк
		if (bank > 80 && bank <= 100) { card.insert(1, "119 27"); } // Газпромбанк Банк
		}
	if (syst > x1 && syst <= x1+x2) {
		card.push_back('5'); // Mastercard
		int bank = GetRandomInt(1, 90);
		if (bank >= 1 && bank <= 30) { card.insert(1, "411 59"); } // ВТБ Банк
		if (bank > 30 && bank <= 60) { card.insert(1, "280 41"); } // Т Банк
		if (bank > 60 && bank <= 90) { card.insert(1, "313 10"); } // Сбер Банк
	}
	if (syst > x1+x2 && syst <= 100) {
		card.push_back('2'); // Mir
		int bank = GetRandomInt(21, 120);
		// if (bank >= 1 && bank <= 20) { card.insert(1, "??? ??"); } // Сбер Банк
		if (bank > 20 && bank <= 40) { card.insert(1, "200 30"); } // Райффайзен Банк
		if (bank > 40 && bank <= 60) { card.insert(1, "200 77"); } // Почта Банк
		if (bank > 60 && bank <= 80) { card.insert(1, "200 70"); } // Т Банк
		if (bank > 80 && bank <= 100) { card.insert(1, "200 01"); } // Газпромбанк Банк
		if (bank > 100 && bank <= 120) { card.insert(1, "202 27"); } // Совком Банк
	}
	std::string ind = std::to_string(GetRandomInt(1000000000, 9999999999));
	card.insert(7, ind);
	card.insert(9, " ");
	card.insert(14, " ");
	card.insert(0, "'");
	card.push_back('\'');
}

void Person::Generate_Person(std::vector<std::string>& male_names_vector,
							std::vector<std::string>& male_surnames_vector,
							std::vector<std::string>& male_midnames_vector,
							std::vector<std::string>& female_names_vector,
							std::vector<std::string>& female_surnames_vector,
							std::vector<std::string>& female_midnames_vector,
							std::vector<std::string>& symptoms_vector,
							std::vector<std::string>& doctors_vector,
							std::vector<std::string>& analyzes_vector, int& x1, int& x2) {
	this->SetId();
	this->count_povtor_visit = 0;
	this->Generate_fio(male_names_vector, female_names_vector,
		male_surnames_vector, female_surnames_vector,
		male_midnames_vector, female_midnames_vector);
	this->Generate_passport();
	this->Generate_snils();
	this->Generate_doctor_symp_an(doctors_vector, symptoms_vector, analyzes_vector);
	this->Generate_date_vis_and_an();
	this->Generate_price();
	this->Generate_card(x1, x2);
}

void Person::Repeat_Person(std::vector<Person>& clinic, int& number,
	std::vector<std::string>& symptoms_vector,
	std::vector<std::string>& doctors_vector,
	std::vector<std::string>& analyzes_vector, int& x1, int& x2) {
	clinic[number].count_povtor_visit += 1;
	clinic[number].Generate_doctor_symp_an(doctors_vector, symptoms_vector, analyzes_vector);
	clinic[number].Generate_new_vis_and_an();
	clinic[number].Generate_price();
	if (clinic[number].count_povtor_visit % 5 == 0) {
		clinic[number].Generate_card(x1, x2);
	}
}

void Person::PrintPerson(std::ofstream& fout) {
	fout << fio << ';' << passport << ';' << snils << ';' << symptoms << ';' << doctor << ';' <<
		timeStruct_vis.tm_year + 1900 << '-' << (timeStruct_vis.tm_mon + 1 < 10 ? "0" : "") << timeStruct_vis.tm_mon + 1 <<
		'-' << (timeStruct_vis.tm_mday < 10 ? "0" : "") << timeStruct_vis.tm_mday << 'T' <<
		(timeStruct_vis.tm_hour < 10 ? "0" : "") << timeStruct_vis.tm_hour << ':' <<
		(timeStruct_vis.tm_min < 10 ? "0" : "") << timeStruct_vis.tm_min << "+03:00" << ';' << analyzes <<
		';' << timeStruct_an.tm_year + 1900 << '-' << (timeStruct_an.tm_mon + 1 < 10 ? "0" : "") <<
		timeStruct_an.tm_mon + 1 << '-' << (timeStruct_an.tm_mday < 10 ? "0" : "") << timeStruct_an.tm_mday <<
		'T' << (timeStruct_an.tm_hour < 10 ? "0" : "") << timeStruct_an.tm_hour << ':' <<
		(timeStruct_an.tm_min < 10 ? "0" : "") << timeStruct_an.tm_min << "+03:00" << ';' << price << ';' << 
		card << std::endl;
}
