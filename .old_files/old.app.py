import os
import re
import math

# =============== PUNKTY =============== 
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

# =============== ZARZADZANIE PLIKIEM =============== 
# Czy plik istnieje? Jeśli nie, to utwórz go
def data_file_exists(file_path):
    if not os.path.exists(file_path):
        print("Warning: Plik data.txt nie istnieje.")
        return 0
    
    else:
        print("Plik data.txt istnieje.")

        with open(file_path, "r") as file:
            content = file.read().strip()
            print("Sprawdzanie zawartości pliku...")

        if re.fullmatch(r"(\d+(\.\d+)?(;(\d+(\.\d+)?))*)?", content):
            print("Plik data.txt zawiera tylko liczby... OK")
            return 1
        else:
            print("Error: Plik data.txt zawiera niepoprawne znaki!")
            return -1

# Import danych z pliku
def data_file_import(file_path):
    labels = ["A", "B", "C", "D"]
    labels_3 = ["A", "B", "C", "D"]

    with open(file_path, "r") as file:
        data = file.read().strip().split(";")
        
    # Filtrujemy dane, pozostawiając tylko liczby
    filtered_data = []
    for value in data:
        try:
            filtered_data.append(float(value))  # Próba konwersji na float
        except ValueError:
            continue  # Jeśli nie uda się przekonwertować, pomijamy wartość
    
    if len(filtered_data) == 8:    
        return {labels[i]: Point(filtered_data[i * 2], filtered_data[i * 2 + 1]) for i in range(4)}, len(filtered_data)
    elif len(filtered_data) == 6:
        return {labels_3[i]: Point(filtered_data[i * 2], filtered_data[i * 2 + 1]) for i in range(3)}, len(filtered_data)
    else:
        print("Error: Plik musi zawierać współrzędne dla 3 lub 4 punktów!")
        return None, len(filtered_data)


# Warunek aby user wprowadził dane x;x;y;y;z;z; a nie xxyyzz
def data_manual_get_valid_input(user_input_prompt):
    while True:
        user_input = input(user_input_prompt).strip()

        # Wymagana poprawność formatu (6 lub 8 liczb oddzielonych średnikami)
        if re.fullmatch(r"(\d+;){5}\d+" , user_input) or re.fullmatch(r"(\d+;){7}\d+", user_input):
            return user_input
        else:
            print("Error: Proszę podać 6 lub 8 liczb oddzielonych średnikami (np. 1;1;2;2;3;3;4;4)")

# Manualne wprowadzenie danych przez użytkownika i wprowadzenie ich do pliku
def data_manual_import(file_path):
    user_choice = input("Czy chcesz wprowadzić dane manualnie? (Y/N): ")
    if user_choice == 'Y':
        data_manual = data_manual_get_valid_input("Wprowadź dane: ")

        with open(file_path, "w") as file:
            file.write(data_manual)
    else:
        print("nie tworzenie pliku")

# Eksport danych do pliku - dopisanie wartości
def data_file_export(file_path, *values):
    with open(file_path, "r") as file:
        lines = file.readlines()

    if lines:
        lines[-1] = lines[-1].strip() + ";" + ";".join(map(str, values)) + "\n"
    else:
        lines.append(";".join(map(str, values)) + "\n")

    with open(file_path, "w") as file:
        file.writelines(lines)        

# =============== ZDEFINIOWANIE FIGURY =============== 

# Typ figury
def polygon_calculate_points(file_path):
    points, pointsCount = data_file_import(file_path)

    if pointsCount == 6 or pointsCount == 8:
        point_a = points.get("A")
        point_b = points.get("B")
        point_c = points.get("C")
        point_d = points.get("D")

    else:
        print("Error: Out of scope")
        exit()

    # Czy występuje kolinearność?
    def polygon_are_collinear(p1, p2, p3, p4=None):
        collinear = p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y)
        return collinear

    if point_d is None: # W przypadku działania na trójkątach
        collinear = polygon_are_collinear(point_a, point_b, point_c)
    else:
        collinear = polygon_are_collinear(point_a, point_b, point_c)
        + polygon_are_collinear(point_a, point_b, point_d)
        + polygon_are_collinear(point_a, point_c, point_d)
        + polygon_are_collinear(point_b, point_c, point_d)
    
    # Jeżeli punkty są kolinearne, to nie tworzą figury
    if collinear == 0:
        print("Error: To nie jest figura!")
        polygon = "to nie jest figura"
        exit()
    else:
        if pointsCount == 6:
            polygon = "trójkąt"
        elif pointsCount == 8:
            polygon = "czworokąt"
        else:
            print("Error: Out of scope")
            polygon = "inny wielokąt"
            exit()

    return polygon

# Obliczenie długości boku
def polygon_distance(p1,p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))

# Typ trójkąta    
def polygon_is_triangle(file_path, epsilon):
    points, _ = data_file_import(file_path)

    point_a = points.get("A")
    point_b = points.get("B")
    point_c = points.get("C")
    
    # Długości boków
    AB = polygon_distance(point_a, point_b)
    BC = polygon_distance(point_b, point_c)
    CA = polygon_distance(point_c, point_a)

    if math.isclose(AB, BC, rel_tol=epsilon) and math.isclose(BC, CA, rel_tol=epsilon):
        polygon_defined = "Trojkat Rownoboczny"
    elif math.isclose(AB**2 + BC**2, CA**2) or math.isclose(AB**2 + CA**2, BC**2) or math.isclose(BC**2 + CA**2, AB**2):
        polygon_defined = "Trojkat Prostokatny"
    elif AB == BC or AB == CA or BC == CA:
        polygon_defined = "Trojkat Rownoramienny"
    else:
        polygon_defined = "Trojkat Roznoboczny"

    return polygon_defined

# Typ czworokąta
def polygon_is_quadrilateral(file_path, epsilon):
    points, _ = data_file_import(file_path)

    point_a = points.get("A")
    point_b = points.get("B")
    point_c = points.get("C")
    point_d = points.get("D")

    # Boki
    AB = polygon_distance(point_a, point_b)
    BC = polygon_distance(point_b, point_c)
    CD = polygon_distance(point_c, point_d)
    DA = polygon_distance(point_d, point_a)

    # Przekątne
    AC = polygon_distance(point_a, point_c)
    BD = polygon_distance(point_b, point_d)

    # Sprawdzanie czy to kwadrat
    if math.isclose(AB, BC, rel_tol=epsilon) and \
          math.isclose(BC, CD, rel_tol=epsilon) and \
          math.isclose(CD, DA, rel_tol=epsilon):
        polygon_defined = "Kwadrat"
    # Sprawdzanie czy to prostokąt
    elif (math.isclose(AB, CD, rel_tol=epsilon) and math.isclose(BC, DA, rel_tol=epsilon)) and \
         math.isclose(AC, BD, rel_tol=epsilon):
        polygon_defined = "Prostokat"
    # Sprawdzanie czy to trapez
    elif (math.isclose(AB, CD, rel_tol=epsilon) and math.isclose(BC, DA, rel_tol=epsilon)) or \
         (math.isclose(AB, DA, rel_tol=epsilon) and math.isclose(BC, CD, rel_tol=epsilon)):
        polygon_defined = "Trapez"
    else:
        polygon_defined = "Inny Czworokat"
    
    return polygon_defined

# Wynikowa figura
def polygon_define_main(file_path, epsilon):
    polygon = polygon_calculate_points(file_path)

    if polygon == "trójkąt":
        polygon_defined = polygon_is_triangle(file_path, epsilon)
    elif polygon == "czworokąt":
        polygon_defined = polygon_is_quadrilateral(file_path, epsilon)

    # Sprawdzanie, czy polygon_defined już istnieje w pliku
    with open(file_path, "r") as file:
        content = file.read().strip()

    # Jeśli polygon_defined nie znajduje się w pliku, dodajemy go
    if polygon_defined not in content:
        data_file_export(file_path, polygon_defined)

# =============== OBLICZENIE POLA I OBWODU FIGURY =============== 
# Obliczenie pola figury
def polygon_calculate_area(file_path, polygon_defined, epsilon):
    points, _ = data_file_import(file_path)

    point_a = points.get("A")
    point_b = points.get("B")
    point_c = points.get("C")
    point_d = points.get("D")

    # Długości boków
    AB = polygon_distance(point_a, point_b)
    BC = polygon_distance(point_b, point_c)
    CA = polygon_distance(point_c, point_a)
    if point_d is not None:
        CD = polygon_distance(point_c, point_d)

    if polygon_defined == "Trojkat Rownoboczny" or "Trojkat Prostokatny" or "Trojkat Rownoramienny" or "Trojkat Roznoboczny":
        half_perimeter = round((AB + BC + CA) / 2, 2)
        area_calculated = math.sqrt(half_perimeter * (half_perimeter - AB) * (half_perimeter - BC) * (half_perimeter - CA))

    elif polygon_defined == "Kwadrat":
        area_calculated = round(AB ** 2, 2)

    elif polygon_defined == "Prostokąt":
        area_calculated = round(AB * BC, 2)

    elif polygon_defined == "Trapez":
        base_a = AB
        base_b = CD
        height = polygon_distance(point_b, point_d)
        area_calculated = round((base_a + base_b) * height / 2, 2)
    else:
        print("Error: Nie udało się obliczyć pola figury")
        exit()
        
    return area_calculated

# Obliczenie obwodu figury
def polygon_calculate_perimeter(file_path, polygon_defined, epsilon):
    points, pointsCount = data_file_import(file_path)

    labels = ["A", "B", "C", "D"]

    if pointsCount == 6: # Dla trójkątów
        perimeter_calculated = sum(polygon_distance(points[labels[i]], points[labels[(i+1)%3]]) for i in range(3))

    elif pointsCount == 8: # Dla czworokątów
        perimeter_calculated = sum(polygon_distance(points[labels[i]], points[labels[(i+1)%4]]) for i in range(4))

    else:
        print("Error: Nieznany typ figury lub nieprawidłowa liczba punktów.")
        exit()

    return perimeter_calculated

# Wynik - eksport do pliku
def polygon_calculate_main(file_path, epsilon):
    polygon_defined = polygon_define_main(file_path, epsilon)

    area_calculated = polygon_calculate_area(file_path, polygon_defined, epsilon)
    perimeter_calculated = polygon_calculate_perimeter(file_path, polygon_defined, epsilon)

    # Eksport wyników do pliku
    data_file_export(file_path, area_calculated)
    data_file_export(file_path, perimeter_calculated)

# =============== MAIN =============== 
def main():
    
    # Deklaracja pliku data.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "data.txt")

    # Czy plik istnieje?
    exists = data_file_exists(file_path)

    if exists == 0: # Gdy plik data.txt nie istnieje
        data_manual_import(file_path)
    elif exists == 1: # Gdy istnieje
        pass
    else: # Gdy są w nim błędy
        exit()

    # Potrzebne do obliczeń
    epsilon = 0.01

    # Główne działanie programu
    polygon_define_main(file_path, epsilon)
    polygon_calculate_main(file_path, epsilon)

    print("Program zakończył działanie...")

# =============== MAIN EXEC =============== 
if __name__ == "__main__":
    main()