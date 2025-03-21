# Logo_Recognition_ML

## Descriere
Proiectul se bazează pe Web-Scrapping pentru a obține logo-urile de pe site-urile companiilor și apoi cu un CNN obținem asimilările și grupam fiecare logo cu compania reprezentativă

## Production-Ready
Solutia este production-ready.
- Proiectul este stabil si functioneaza in toate conditiile
- Este scalabil și optimizat pentru mediile de producție.
- Documentația completă este inclusă pentru deployment și mentenanță.

## Thought Process
1.	Am incercat sa vad cum as putea sa fac web scraping, specific pentru logo-uri. Vazand ca exista tool-uri in python, fiind familiar cu limbajul, am decis ca python, in speta Jupyter Notebook fiind mai usor de vizualizat output urile, va fi principala mea solutie la problema. 
2.	Am incercat un tool numit BeautifulSoup, dar am observat ca acest tool poate face web-scrapping doar pe site uri html statice, asa ca am mai cautat si alte tool uri pe care le pot integra in cod. M am gandit ca am nevoie de ceva care sa recunoasca site-uri JS based si am gasit Selenium. Era o diferenta dar din pacate nu mi lua atat de multe site-uri din cauza protocoalelor de accesare ale acestora. Asa am mai gasit tool uri care sa incerce HTTP sau HTTPS si sa treaca de anumite bariere de intrare in site cu ajutorul package -ului selenium-stealth. Am adaugat si un API gratis foarte bun numit Clearbit in script si un detector de iconite favicon.io pentru a include toate posibilitatile de implementare ale logo-urilor ale fiecarui site.
3.	Dupa ce am adunat cate logo-uri am putut, am incercat sa implementez un model de CNN pre-trained MobileNetV2 si am pus logo-urile care au asemanari sa fie puse pe cate un cluster. Acest lucru a functionat in mare parte dar nu putea sa mi grupeze fiecare logo in firma care reprezinta si uneori dadea rateuri. Asa ca am venit cu o alta solutie care consta in schimbarea modelului pre-trained, ci anume ResNet si adaugarea in script la o solutie simpla si aceea este ca daca doua imagini sunt asemanatoare si au un numele png-ului acelasi keyword (adica aceeasi firma spre exemplu aamco) se va forma un folder cu numele firmei si cu logo-urile corespunzatoare

### Abordare Tehnică
- **Arhitectură:** Am folosit Web-scrapping tools  pentru a prelua logo-urile prezentate in site-uri.
- **Decizii de proiectare:** Am ales Tensorflow, Pytorch si script de ordonare a folderelor cu numele firmelor principale bazat pe keywords pentru a gasi asemanari in feature-uri si in numele file-urilor.
  
### Provocări și Soluții
- Provocarea A: Până în acest moment nu am avut constințe în ceea ce privește cum se realizează un script de Web-Scrapping în Python
- Soluția: Sursele de informare au fost: stackoverflow, tutoriale, documentatie oficiala  ale tool-urilor și chatgpt pentru implementarea corectă a acestora 
- Provocarea B: Script-ul nu funcționa pe majoritatea site-urilor date de file-ul logos.snappy.parquet 
- Soluția: Am identificat erorile din output si am observat ca script-ul funcționeaza doar pentru pagini html statice. Astfel, am cautat cat mai multe tool-uri care sa acopere orice scenariu, am identificat 3 scenarii posibile precum: site-ul este JS based, iconita este favicon.io si implementarea  unui API gratis foarte bun in a detecta logo-uri.
- Provocarea C: Care este cea mai buna solutie pentru a grupa logo-urile cu firmele pe care le reprezinta
- Soluția: Am incercat doua modele de AI pre-trained, acelea fiind MobileNetV2 si ResNet. ResNet in acest caz a fost mult mai eficient. Pentru gruparea mai precisa a logo-urilor, am folosit un Python script care determina locul  unde pot fi inserate imaginile în functie de  asemanarile dintre ele, marcând in egala masura daca acestea corespund unor firme asemanatoare și  creand automat un folder cu firma respectiva.

## Work Ethic
- Am urmat bunele practici de dezvoltare, inclusiv code reviews și testare continuă.
- Sunt dedicat menținerii unui cod curat și documentat.
- Mă angajez să continui îmbunătățirea soluției prin feedback și actualizări regulate.
