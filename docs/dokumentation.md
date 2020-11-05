---
permalink: /dokumentation/
title: "Dokumentation"
---

Der folgende Artikel zeigt die einzelnen Schritte auf die angewandt wurden, um das Friedhofsregister der jüdischen Gemeinde zu Strelitz so aufzubereiten, dass es volltextdurchsuchbar, maschinenlesbar, XML-annotiert und im Ausgangsformat als TEI/XML sowie ALTO verfügbar ist. Am Ende stehen zwei „Produkte“: Einerseits die Ansicht des TEIs im Deutschen Textarchiv, zur Korrektur und vollen Nutzbarkeit des TEI; andererseits die Ansicht im DFG-Viewer mittels generierter METS, zur zeilengenauen Ansicht des transkribierten Textes.  
Es wurde der Versuch unternommen, die dafür notwendigen Schritte und verwendeten Tools bestmöglichst zu erläutern. Ein kurzer historischer Abriss zur jüdischen Gemeinde zu Strelitz, der auch die Motivation dieses Vorhabens begründet, findet sich unter dem Menüpunkt [„Über das Friedhofsregister“](docs/about.md).

 1. [Preprocessing](#preprocessing)
 2. [Layouterkennung, Transkription und Annotation in Transkribus](#transkribus)
 3. [Postprocessing – der Weg zum TEI](#postprocessing)
 4. [Generierung der METS aus ALTO](#mets)
 5. [Ausblick](#ausblick)

    
<h2 id="preprocessing">Preprocessing</h2>

Wie bereits erwähnt, befindet sich das Friedhofsregister der jüdischen Gemeinde zu Strelitz als Mikroverfilmung im Archiv des Leo Baeck Institutes in New York. Etliche Nachlässe und darin befindliche Archivalien wurden bereits digitalisiert<sup id="a1">[1](#f1)</sup> und werden über [archive.org](https://archive.org/) gehostet. Das Friedhofsregister wurde im Zuge des Preprocessings als JPEG konvertiert und mit *[ScanTailor](https://scantailor.org/)* aufbereitet. Darunter fallen die standardmäßigen Vorarbeiten, wie das Korrigieren der Bildausrichtung, der Helligkeit und das Zuschneiden der einzelnen Digitalisate.

<h2 id="transkribus">Layouterkennung, Transkription und Annotation in Transkribus</h2>

In *Transkribus* sind mittlerweile viele unterschiedliche Modelle zur Layouterkennung verfügbar. Für den Anwendungsfall der Friedhofregisters war eine doppelspaltige Erkennung notwendig, welche die einzelnen Sterbeeinträge nochmals in einzelne Texregionen einteilt. Keines der zur Zeit verfügbaren Modelle konnte diese Aufgaben erfüllen<sup id="a2">[2](#f2)</sup>. Jeder Eintrag muss sich in einer eigenen Textregion befinden, da im XML-basierenden Ausgabeformat damit automatisch ein eigenständiger Paragraph, also `<p>`, versehen ist. An dieser Stelle musste also händisch nachgearbeitet werden, jedoch erleichtern die Werkzeuge zum „Zerlegen” (horizontal/vertikal) einer Textregionen die Arbeit enorm, sodass eine Textregion, welche die komplette Seite erfasst, relativ schnell entsprechend zugeschnitten werden kann. Die Zeilenerkennung der verfügbaren Modelle läuft ziemlich zuverlässig und bedarf nur wenig Korrektur. Eine „line” und damit verbundene „baseline” ergeben im späteren Ausgabeformat automatisch ein `</lb>`, einen Zeilenumbruch.

  

![Bearbeitung der automatischen Layouterkennung in *Transkribus*](https://i.imgur.com/GP8uvUb.png)

Bei der Korrektur der Layouterfassung wurde den einzelnen Textregionen und Zeilen noch eine ID zugewiesen, die entsprechend der Readingorder numerisch aufsteigend verläuft. *Transkribus* weist zwar jeder Textregion und Zeile automatisch eine ID zu, aber für die Nachbearbeitung ist es nützlicher eine schlichte und leicht identifizierbare ID, wie bspw. `r1|3`, zu haben. Die erste Nummer steht dabei für die (Text)Region und die zweite für die Zeile. Auch das lässt sich in *Transkribus* automatisch realisieren; ein Klick innerhalb des Tabs „Layout“ auf „Assign unique IDs [...]“ benennt die IDs entsprechend der Readingorder um.

In *Transkribus* gibt es eine Fülle an unterschiedlichsten HTR-Modellen zur Handschriftenerkennung. Besonders der Zeitraum des 18. und 19. Jahrhunderts ist dabei gut abgedeckt. Naturgemäß ähneln sich zwar die Stile der Kurrentschrift unterschiedlicher „Hände“, bedürfen aber nichtsdestotrotz, insbesondere bei „krakeliger“ und untrainierter Handschrift, einer Nachbearbeitung.

Nach der vollständigen Layouterfassung und Transkription wurden die erste Annotation für die spätere Ausgabe im (TEI-)XML vorgenommen. *Transkribus* verfügt über ein bereits angelegtes Set an Tags, NutzerInnen können sich aber auch ihr Tagset selbst zusammenstellen und mit einer entsprechenden Tastenkombination anwenden (ALT+x).

Für das Friedhofsregister wurde die standardmäßige Annotation wie `<persName>`, `<date>`, `<placeName>` etc. vorgenommen.

![Ansicht des XML-Taggings in Transkribus](https://i.imgur.com/JDdIsr7.png)

Jeder Sterbe- bzw. Beerdigungseintrag hat eine Nummer. Im anhängenden alphabetischen Register lassen sich diese Nummern wiederfinden. Damit eine spätere Verknüpfung von Name bzw. Nummer im Register und dem eigentlichen Sterbeeintrag vorbereitet werden konnte, wurde jeder Nummer eines Eintrags ein `<label>`, und analog dazu den Nummern im alphabetischen Register ein `<ref>` zugewiesen.

Das nun komplette und annotierte Dokument wurde schließlich in page-XML und ALTO exportiert.

<h2 id="postprocessing">Postprocessing – der Weg zum TEI</h2>

Da am Ende zwei Ergebnisse stehen sollten, „trennen“ sich hier die Wege der Nachbearbeitung. Für die Ansicht im DFG-Viewer stehen die Formate ALTO und METS nebeneinander – sie spielen in diesem Schritt keine Rolle mehr. Für die volle Nutzbarkeit der Annotationen innerhalb des XML/TEI wird jedoch das DTA verwendet. Hierzu wird ein valides TEI gemäß des DTA-Basisformats benötigt<sup id="a3">[3](#f3)</sup>. Aus den exportierten page-XMLs aus *Transkribus* wurde nun ein zusammenhängendes TEI geschaffen. Mittels *page2tei*<sup id="a4">[4](#f4)</sup> lässt sich das relativ einfach realisieren. Neben dem verfügbaren Paket auf GitHub wird noch der XSLT- und XQuery-Prozessor *Saxon* zur Transformation benötigt<sup id="a5">[5](#f5)</sup>. Exportiert man aus *Transkribus* die page-XML- und METS-Dateien kann dann folgender Befehl ausgeführt werden:

    $ java -jar saxon9he.jar -xsl:page2tei-0.xsl -s:mets.xml -o:friedhofsregister_strelitz.xml

Nun ist ein zusammenhängendes TEI aus den page-XML-Dateien generiert worden.  

Zuerst wurde eine Unterteilung des Registers vorgenommen. Die Seiten 1 bis 65 sind Sterbeeinträge, die Seiten 66 bis 96 bilden das alphabetische Register. Gemäß des DTA-Basisformats wurden diese beiden Einheiten mittels `<div>` umschlossen, wobei das alphabetische Register noch um das Attribut `@type=”index”` erweitert wurde. Der Inhalt der beiden Abschnitte wurde mittels `<head>` ausgezeichnet<sup id="a6">[6](#f6)</sup>.

Da jeder Eintrag mit einer Textregion und damit einem `<p>` umkapselt ist, wurde von jedem beginnenden bis endenden `<p>`, das Tag `<item>`<sup id="a7">[7](#f7)</sup> umschlossen. Das Umschließen mit dem Tag <item> konnte erst in diesem Schritt, und nicht in *Transkribus* selber, vorgenommen werden. *Transkribus* hat nämlich den Nachteil, dass sobald mehrere aufeinanderfolgende Zeilen markiert und dann annotiert werden, das jeweilige Tag bei jeder Zeile neu beginnt und schließt:

~~~ xml
<persName>Esther Hirsch</persName></lb>
<persName>gb. Jacob</persName>
~~~

Für die Wohlgeformheit des TEI sollte jedoch ein Tag, in diesem Fall das Tag `<persName>`, auch trotz Zeilenumbruch einmal umschließend gesetzt werden. Daher wurde im Nachgang mit regulären Ausdrücken gearbeitet<sup id="a8">[8](#f8)</sup>. In diesem Beispiel:

Suche nach `</persName>(\s*<lb[^>]*/>\s*)<persName>` und ersetze durch `$1`.

Das Ergebnis sieht wie folgt aus:
~~~xml
<persName>Esther Hirsch</lb>
gb. Jacob</persName>
~~~
Selbiges gilt für `<placeName>` und andere Auszeichnungen, die sich über mehr als eine Zeile erstrecken und durch ein `</lb>` getrennt sind.

Daher wurde auch die Umschließung einer Textregion `</p>` mit `</item>` erst im transformierten XML/TEI vorgenommen. Der reguläre Ausdruck dafür lautet:

Suche nach `(<p\b[^>]*>.*?</p>)` und ersetze durch `<item>$1</item>`.

Das Ergebnis sieht wie folgt aus:
~~~xml
<item>
	<p>
	<label>43</label></lb>
		<persName>Esther Hirsch</lb>
		gb. Jacob</persName></lb>
		gest. <date>23.t April 1782</date></lb>
	</p>
</item>
~~~

Einem `<item>` wurde nun eine genaue xml:id zugewiesen, die sich aus dem Tag `<label>` innerhalb eines `<item>` ergibt. Ein dafür angefertigtes Perl-Skript<sup id="a9">[9](#f9)</sup> liest in jedem Eltern-Element `<item>` das Kind-Element `<label>` aus und weist die entsprechende Nummer als `xml:id` zu. Das Perl-Skript ignoriert dabei die inkonsequente Nummerierung im Friedhofsregister wie bspw. „No 1” vs „1” und generiert die xml:id nur aus den numerischen Werten. Da eine xml:id keine Ziffern an erster Stelle haben darf, wurde der xml:id ein Buchstabe vorangestellt. Damit sind nun `<ref>` und `<item>` genau miteinander verbunden.

Da alle Einträge einem Listenschema folgen, wurden sie vollständig mit dem Tag `<list>` umschlossen, die Paginierung auf jeder einzelnen Seite mit einem `<fw>`. Da sich die Paginierung immer oben befindet und als Folierungsnummer dient, wurden `<fw>` um die Attributwerte `@place="top"` und `@type="folNum"` erweitert.

Die Personenname und das damit verbundene Tag `<persName>` wurde, sofern sinnvoll und möglich, mit dem Attribut `@ref` erweitert. Als ref-Wert wurde eine standardmäßige Verlinkung zur entsprechenden GND<sup id="a10">[10](#f10)</sup> verwendet. Für den ref-Wert des `</placeName>` wurde GeoNames<sup id="a11">[11](#f11)</sup> genutzt.

  

Einige Beerdigungseinträge führen auch den Beruf oder Funktion innerhalb der Gemeinde auf. Da `<occupation>` innerhalb von `<item>` nicht zulässig ist und in vielen Fällen wie „Gemeindediener“, „Rabbi“ oder „Ältester“ auch nicht passend erscheint, wurden diese Bezeichnungen mit `<roleName>` ausgezeichnet.

Die hebräischen Anmerkungen wurden mittels `<foreign>` und dem Attributwert `@xml:lang="hbo">`<sup id="a12">[12](#f12)</sup> umschlossen. 

Letztlich wurde noch der TEI-Header gemäß des DTABfs angepasst und einige Metadaten, wie etwa <repository> für das besitzende Instituts der Vorlage oder <author> für den Herausgeber des Registers, angepasst.

<h2 id="mets">Generierung der METS aus ALTO</h2>

Die Formate ALTO und METS stehen parallel nebeneinander. Die einzelnen ALTO-XMLs konnten wie bereits im vorherigen Abschnitt beschrieben, aus *Transkribus* exportiert werden. ALTO enthält im XML Schema alle verfügbaren Daten des Layouts der zugrundeliegenden Vorlage.

Im Falle des Friedhofsregister sind dabei vor allem die Maße und Positionen der einzelnen Sterbeeinträge als `<TextBlock>` sowie die darin befindlichen einzelnen Zeilen samt ihrem transkribierten Inhalt als `<TextLine>` relevant. Eine einzelne Zeile ist in ALTO dann wie folgt strukturiert:

~~~xml
<TextLine ID="r1l2"
BASELINE="183"
HEIGHT="123"
WIDTH="572"
VPOS="60"
HPOS="62">
<String ID="string_r1l2"
HEIGHT="123"
WIDTH="572"
VPOS="60"
HPOS="62"
CONTENT="Mendel Strelitz"/>
</TextLine>
~~~

die METS-Datei wurde wurde mittels *tei2mets*<sup id="a13">[13](#f13)</sup> generiert. In ihr befinden sich alle relevanten Metadaten über das Friedhofsregister.

Nun sind durch die Formate ALTO und METS der transkribierte Text exakt mit den Bildigitalisaten verbunden. Im DFG-Viewer lässt sich das Ergebnis anschauen; die „Maschine“ weiß also, welche Textregion und welche Textzeile zu welcher Position innerhalb des Bildes gehört.

Unter www lässt sich nun das Register samt Volltext im DFG-Viewer betrachten.

<h2 id="ausblick">Ausblick</h2>

Die Datumsangaben sind bisher lediglich mit `<date>` umschlossen, eine Erweiterung um das Attribut `@when` wäre zur maschinellen Verarbeitung der Daten denkbar. Dabei folgt die Angabe des Datums dem Schema `YY-MM-DD`, also bspw:  
~~~xml
<date when="1822-11-02">2t Novbr 1822</date>
~~~
  
Auch eine Auszeichnung mit dem Tag `<death>` und dem Attribut `@when` ist möglich. In einigen Fällen ist auch das Geburtsdatum angegeben, diese könnten dann analog durch `<birth>` und `@when` ausgezeichnet werden.

Neben den Datumsangaben die dem System des gregorianischen Kalenders folgen, finden wir auch Daten gemäß des jüdischen Kalenders. 

Im Friedhofsregister lassen sich auch einige Personen finden, die für das jüdische Leben in Deutschland überregionale Bedeutung erlangt haben. So ist z.B. der damalige Landesrabbiner von Mecklenburg-Strelitz, [Jacob Hamburger](https://de.wikipedia.org/wiki/Jacob_Hamburger), dort verzeichnet. Auch verzeichnet ist bspw. der vermeintlichen Gründer der Strelitzer jüdischen Gemeinde und „Hofjude“ des Herzogs Adolph III zu Mecklenburg. In Tychsens drittem Teil seiner *Nebenstunden* heißt es dazu:

> Um das Jahr 1608 hatten auch der damalige Herzog zu Strelitz Adolph
> II. einen Hofjuden Namens R. Iakof aus Frankfurt an der Oder, und
> dessen Gemahlin geb. Prinzess. aus Sondershausen einen Agenten
> Alexander aus Sondershausen, in ihren Diensten. Nach ihrem Tode wurde
> der Knecht des obbemeldeten Iakof, Namens Wolf Hofjude bey Herzog
> Adolph III. Durch diesen Wolf ist die jüdische Gemeine in Strelitz
> eigentlich gestiftet.<sup id="a14">[14](#f14)</sup>

Aller Wahrscheinlichkeit nach ist dieser „Hofjude“ Wolf, Wolff Jacob (Nr. 5 im Register). Er verstarb im Januar 1743 und wurde auf dem Strelitzer Friedhof beerdigt.

Da die Daten im Repositorium sowie im Deutschen Textarchiv stehen unter der Lizenz CC BY-SA 4 und sind damit für jeden einsehbar und können beliebig nachgenutzt werden. Inbesondere die Transkription und Übersetzung der Anmerkung in hebräischer Sprache bedürfen noch freiwilligen Helferinnen und Helfern. Dazu benötigt man lediglich einen Account für die [Qualitätssicherung](http://www.deutschestextarchiv.de/dtaq/book/view/jacobson_strelitzfriedhofsregister_1929) des DTAs sowie eine kurze Mail an das Team<sup id="a15">[15](#f15)</sup> und man wird für die Bearbeitung freigeschaltet.

Ein spannender Datensatz mit viel Potential.

---

<b id="f1">1</b> Als ausgezeichnete Metasuchmaschine für Archivalien deutsch-jüdischen Ursprungs eignet sich die Datenbank vom Center for Jewish History, [https://www.cjh.org/](https://www.cjh.org/), hierüber lassen sich Archivalien, welche auch im großen Umfang bereits digitalisiert wurden, auffinden. Bei der Recherche sind die Bestände der Nationalbibliothek von Israel, [https://web.nli.org.il](https://web.nli.org.il), von ebenso großer Bedeutung, ebenso wie das Central Archives for the History of the Jewish People (CAHJP), [http://cahjp.nli.org.il/](http://cahjp.nli.org.il/), welches zum größten Teil die (Teil-)Nachlässe jüdischer Gemeinde in Deutschland verwahrt.  [↩](#a1)

<b id="f2">2</b> Zum Trainieren eigener Layouterkennungs-Modelle eignet sich das Tool [P2PaLA](https://github.com/lquirosd/P2PaLA); eine Einbettung in die Software *Transkribus* hat bereits stattgefunden und wird laufend ausgebaut. [↩](#a2)

<b id="f3">3</b> s. dazu die Dokumentation des DTABfs unter [http://www.deutschestextarchiv.de/doku/basisformat/](http://www.deutschestextarchiv.de/doku/basisformat/). [↩](#a3)

<b id="f4">4</b> [https://github.com/dariok/page2tei](https://github.com/dariok/page2tei). [↩](#a4)

<b id="f5">5</b> [https://www.saxonica.com](https://www.saxonica.com). [↩](#a5)

<b id="f6">6</b> s. dazu auch den Abschnitt *Texteinteilung auf Kapitelebene* unter [http://www.deutschestextarchiv.de/doku/basisformat/div.html](http://www.deutschestextarchiv.de/doku/basisformat/div.html). [↩](#a6)

<b id="f7">7</b> s. hierzu auch die Empfehlungen der TEI unter [https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-item.html](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-item.html). [↩](#a7)

<b id="f8">8</b> Um reguläre Ausdrücke zu testen bzw. zu erstellen, eignet sich die Webanwendung *regex101* ausgezeichnet, siehe [https://regex101.com](https://regex101.com). [↩](#a8)

<b id="f9">9</b> Das Skript wurde von Frank Wiegand geschrieben und findet sich auf GitHub, [https://gist.github.com/haoess/77e1eda37fa18fe764d76dbc7b4e9240](https://gist.github.com/haoess/77e1eda37fa18fe764d76dbc7b4e9240). [↩](#a9)

<b id="f10">10</b> Gemeinsame Normdatei, siehe [https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html](https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html). [↩](#a10)

<b id="f11">11</b> s. [https://www.geonames.org](https://www.geonames.org). [↩](#a11)

<b id="f12">12</b> Der Wert für fremdsprachliches Material ist das Kürzel internationale Norm ISO 639-3, in diesem Fall handelt es sich um rabbinisches Hebräisch. [↩](#a12)

<b id="f13">13</b> s. dazu [https://github.com/tboenig/tei2mets](https://github.com/tboenig/tei2mets) von Matthias Boenig [↩](#a13)

<b id="f14">14</b> vgl. Tychsen, Oluf Gerhard: Bützowische Nebenstunden. Dritter Theil, Bützow 1768, S.5. [Online verfügbar Rostocker Dokumentenserver.](http://rosdok.uni-rostock.de/resolve/id/rosdok_document_0000016029)  [↩](#a14)

<b id="f15">15</b> Eine Mail an dtakorrektur(at)bbaw.de mit dem kurzen Hinweis auf das Friedhofsregister reich dazu völlig. [↩](#a15)

