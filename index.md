Der folgende Artikel zeigt die einzelnen Schritte auf die angewandt wurden, um das Friedhofsregister der jüdischen Gemeinde zu Strelitz so aufzubereiten, dass es volltextdurchsuchbar, maschinenlesbar, XML-annotiert und im Ausgangsformat als TEI/XML sowie ALTO verfügbar ist. Am Ende stehen zwei „Produkte“: Einerseits die Ansicht des TEIs im Deutschen Textarchiv<sup id="a1">[1](#f1)</sup>, zur Korrektur und vollen Nutzbarkeit des TEI; andererseits die Ansicht im DFG-Viewer mittels generierter METS, zur zeilengenauen Ansicht des transkribierten Textes.
Es wurde der Versuch unternommen, die dafür notwendigen Schritte und verwendeten Tools bestmöglichst zu erläutern. Ein kurzer historischer Abriss zur jüdischen Gemeinde zu Strelitz wird die Motivation für dieses Vorhabens begründen und den Artikel einleiten.

 1. [Zur Geschichte des der jüdischen Gemeinde und des Friedhofs in Strelitz](#geschichte)
 2. [Allgemeines zum Friedhofsregister](#allgemeines)
 3. [Preprocessing](#preprocessing)
 4. [Layouterkennung, Transkription und Annotation in Transkribus](#transkribus)
 5. [Postprocessing – der Weg zum TEI](#postprocessing)
 6. [Generierung der METS aus ALTO](#mets)
 7. [Ausblick](#ausblick)

    

<h2 id="allgemeines">
Zur Geschichte des der jüdischen Gemeinde und des Friedhofs in Strelitz
</h2>

Die jüdische Gemeinde zu Strelitz (heute Strelitz-Alt, Stadtteil von Neustrelitz) in Mecklenburg war im Laufe ihres Bestehens, insbesondere im 19. Jahrhundert, eine der größten jüdischen Gemeinden Mecklenburgs.

Die Einweihungsfeier zur ersten Synagoge in Strelitz fand am 5. September 1763 statt<sup id="a2">[2](#f2)</sup>. Zu dieser Zeit lebten bereits etwa 130 jüdische Familien in Strelitz<sup id="a3">[3](#f3)</sup>.

Der Herzog zu Mecklenburg, Adolf Friedrich III., gewährte im 18. Jahrhundert immer mehr Personen jüdischen Glaubens die Ansiedlung im Herzogtum. In diesem Zusammenhang kann man schon fast von einer Förderung der Zuwanderung sprechen, denn der Herzog und die Landesregierung erhofften sich dadurch eine wirtschaftliche Stärkung des Herzogtums. Zum einen sollten die jüdischen Kaufleute und Händler die Region wirtschaftlich stärken, zum anderen zahlten sie aber auch eine Schutzsteuer, eine jährliche (teilweise auch vierteljährliche) Zahlung, die ihnen erlaubte, dass sie überhaupt kaufmännisch tätig werden und in der Region einen Wohnsitz schaffen konnten. Dieses landesherrliche Privileg erteilte ihnen damit die Konzession geregelter Arbeit nachzugehen und sich niederzulassen. Gleichzeitig sollten sie aber auch nicht in zu starke Konkurrenz mit christlichen Kaufleuten treten. Die herzogliche Landesregierung stellte diese Schutzbriefe zwar aus, sofern erwartbar war, dass der Antragstellende zukünftig wirtschaftlich unabhängig sein würde, war aber ganz im Geiste der Zeit antisemitisch vorurteilsbehaftet und fürchtete um die kaufmännische Existenz der christlichen Bevölkerung.

Das Gesuch des Vaters von Daniel Sanders, Hendel Sanders, im Jahr 1808 zeigt exemplarisch wie die Landesregierung auf die Bitte um Erlaubnis mit Tabak und Leder handeln zu dürfen, dem Herzog Karl II., reagiert und Mitteilung macht:

  

> Ueberdies haben Ew. Herzog. Duchl. bei gnädigster Ertheilung der
> Schutzbriefe an die Juden unsers Wissens stets die Regel beobachtet,
> die selben nur auf kleinen Handel im Allgemeinen zu concessionieren
> [...] Leider sehen wir zwar vor Augen daß diese Höchste Absicht nicht
> erreicht wird weil die Juden nach ihner bekannten Denkungsart, wonach
> sie, wenn ihnen der Finger zu nehmen concedirt wird, nach dem ihnen
> stets beiwohnenden Dünkel, sich die ganze Hand bedienen.<sup id="a4">[4](#f4)</sup>

Sanders erhält schließlich sein „Privileg“ und wird Schutzjude, der Handel mit Tabak wird ihm jedoch nicht gestattet.

1802 waren es schon etwa 800 Menschen israelitischen Glaubens, die in Mecklenburg-Strelitz lebten – davon allein 600 in Strelitz<sup id="a5">[5](#f5)</sup>.  

Der jüdische Friedhof in Strelitz war einer der ältesten in ganz Mecklenburg und wurde 1728 angelegt. Der Friedhof ist heute nicht mehr existent; es stehen zwar noch zwei Grabsteine, diese sind aber umgebettet worden und dienen eher repräsentativen Charakter. Das Dritte Reich überstand der Friedhof wohl nahezu unbeschadet, die Angaben hierzu sind allerdings sehr unterschiedlich. In der Neustrelitzer Ausgabe der „Landeszeitung“ heißt es in einem Artikel vom 9. September 1949: 

> Als in der berüchtigten Kristallnacht 1938 [...] braun-uniformierte
> Nazirowdys die Friedhofsmauer stürmten und sich auf dem Friedhof
> selbst [...] schlimmer als Barbaren benahmen, war es um die
> Sehenswürdigkeit des Alt Strelitzer Judenfriedhofs geschehen [...].
> Der Friedhof wurde zum Spiegel der faschistischen Willkür

Nichtsdestotrotz ist davon auszugehen, dass viele Grabsteine die Verwüstungen überstanden und die größten Schäden durch äußere Witterungseinflüsse und mangelnde Instandhaltung und Pflege des Areals entstanden.

Der Bezirkskonservator für Vor- und Frühgeschichte schreibt im Juli 1950 an den Rat der Stadt Neustrelitz, dass sich der jüdische Friedhof in einem entsetzlichen Zustand befinde und man diesen Missstand dringend beheben müsse – er würde sich für Neustrelitz schämen. Die gewünschte Aufräumarbeiten finden wohl auch zeitnah durch eine ortsansässige FDJ-Gruppe statt.

Kaum nachvollziehbar scheint es daher, dass wenige Jahre später, Ende 1950er Jahre, von der Bezirksregierung entschieden wird, dass die Grabsteine zu entfernen und das Gelände zu räumen ist, auch Stelen und Obelisken sollen zerschlagen werden. Die Grabsteine wurden zertrümmert, als Pflastersteine benutzt oder gleich im Hafen versenkt – bis heute scheint nicht genau klar zu sein, aus welchen Beweggründen damals so gehandelt wurde<sup id="a6">[6](#f6)</sup>.

Mit dem materiellen Verlust der Grabsteine ging auch das Wissen darüber verloren, um welche Personen es sich handelt, deren letzten 100 erhaltenen Grabsteine bis zum Tage der „Räumung“ noch vorhanden waren. Überhaupt schien es so, als sei ein Seelen-, Sterbe- oder Beerdigungsregister nicht ausfindig zu machen, und das obwohl die Gemeinde zu Strelitz doch so groß war und manche ihre Mitglieder es zur überregionalen Bekanntheit brachten.

Zwar tauchten immer wieder einige kleine Verzeichnisse auf, wer die letzten Gemeindemitglieder waren und auch, wann diese beerdigt wurden, ein Gesamtverzeichnis, ein Beerdigungsregister, war der Öffentlichkeit aber nicht bekannt. Dabei hatte Jacob Jacobson, der bis 1939 das Gesamtarchiv der deutschen Juden leitete, vermutlich noch in der Zeit vor der „Machtergreifung“ eine Abschrift angefertigt, welche die Bestattungen der jüdischen Gemeinde zu Strelitz dokumentiert. Wovon Jacobson genau seine Abschrift anfertigte, was also seine zugrunde liegende Originalquelle war, ist bisher nicht genau geklärt<sup id="a7">[7](#f7)</sup>. Auch ist im Register ein deutlicher Wechsel der Handschrift zu erkennen – er fertigte diese also nicht allein an.

Das Leo Baeck Institute hat jedoch die Abschrift von Jacobson mikroverfilmt und als Digitalisat zur Verfügung gestellt<sup id="a8">[8](#f8)</sup>. Basierend auf diesen Digitalisaten wurde das Beerdigungsregister in verschiedenen Schritten aufbereitet, sodass nun eine XML/TEI und ALTO-Version des Registers zur Verfügung steht, die volltextdurchsuchbar, maschinenlesbar und strukturiert über 250 Jahre einen Teil des jüdischen Lebens in Strelitz wiedergibt.

<h2 id="geschichte">Allgemeines zum Friedhofsregister</h2>

Das Friedhofsregister der Gemeinde zu Strelitz ist inhaltlich ebenso strukturiert wie viele andere Kirchenbücher christlicher Gemeinden in Deutschland. Chronologisch verzeichnet es die jeweiligen Sterbefälle und gibt zu jeder Person individuell weitere Informationen, wie Beruf, Geburtsdatum, Alter oder verwandtschaftliche Beziehungen. Die Einträge sind in ihrem Umfang nicht immer einheitlich, der Grad der eingetragenen Informationen hängt – genau so wie in christlichen Geburts-, Ehe- oder Sterberegistern – immer von der jeweiligen schriftführenden Person ab. Vorteilhaft am Register der Strelitzer Gemeinde ist das alphabetische Register am Ende, wenngleich es auch nicht immer konsistent angelegt ist, lassen sich doch durch die einzelnen Nummern der Einträge schnell einzelne Personen auffinden. Eine Besonderheit stellen die Vermerke in hebräischer Sprache dar. Auch hier ist der Informationsgehalt unterschiedlich und ändert sich im Laufe der Jahrzehnte. Teilweise geben sie nur das bereits in lateinischen Buchstaben geschrieben wieder, teilweise ergänzen sie verwandtschaftliche Beziehungen. Im Laufe der Jahrzehnte werden diese Vermerke immer seltener, sodass ab etwa 1869 neben den angegebenen Datum, meistens das Sterbedatum, teilweise aber auch das Geburtsdatum, nur noch der Tag des Todes gemäß des jüdischen Kalenders niedergeschrieben wurde.


<h2 id="preprocessing">Preprocessing</h2>

Wie bereits erwähnt, befindet sich das Friedhofsregister der jüdischen Gemeinde zu Strelitz als Mikroverfilmung im Archiv des Leo Baeck Institutes in New York. Etliche Nachlässe und darin befindliche Archivalien wurden bereits digitalisiert<sup id="a9">[9](#f9)</sup> und werden über [archive.org](https://archive.org/) gehostet. Das Friedhofsregister wurde im Zuge des Preprocessings als JPEG konvertiert und mit *[ScanTailor](https://scantailor.org/)* aufbereitet. Darunter fallen die standardmäßigen Vorarbeiten, wie das Korrigieren der Bildausrichtung, der Helligkeit und das Zuschneiden der einzelnen Digitalisate.

<h2 id="transkribus">Layouterkennung, Transkription und Annotation in Transkribus</h2>

In *Transkribus* sind mittlerweile viele unterschiedliche Modelle zur Layouterkennung verfügbar. Für den Anwendungsfall der Friedhofregisters war eine doppelspaltige Erkennung notwendig, welche die einzelnen Sterbeeinträge nochmals in einzelne Texregionen einteilt. Keines der zur Zeit verfügbaren Modelle konnte diese Aufgaben erfüllen<sup id="a10">[10](#f10)</sup>. Jeder Eintrag muss sich in einer eigenen Textregion befinden, da im XML-basierenden Ausgabeformat damit automatisch ein eigenständiger Paragraph, also `<p>`, versehen ist. An dieser Stelle musste also händisch nachgearbeitet werden, jedoch erleichtern die Werkzeuge zum „Zerlegen” (horizontal/vertikal) einer Textregionen die Arbeit enorm, sodass eine Textregion, welche die komplette Seite erfasst, relativ schnell entsprechend zugeschnitten werden kann. Die Zeilenerkennung der verfügbaren Modelle läuft ziemlich zuverlässig und bedarf nur wenig Korrektur. Eine „line” und damit verbundene „baseline” ergeben im späteren Ausgabeformat automatisch ein `</lb>`, einen Zeilenumbruch.

  

![Bearbeitung der automatischen Layouterkennung in Transkribus](https://i.imgur.com/GP8uvUb.png)

Bei der Korrektur der Layouterfassung wurde den einzelnen Textregionen und Zeilen noch eine ID zugewiesen, die entsprechend der Readingorder numerisch aufsteigend verläuft. Transkribus weist zwar jeder Textregion und Zeile automatisch eine ID zu, aber für die Nachbearbeitung ist es nützlicher eine schlichte und leicht identifizierbare ID, wie bspw. `r1|3`, zu haben. Die erste Nummer steht dabei für die (Text)Region und die zweite für die Zeile. Auch das lässt sich in Transkribus automatisch realisieren; ein Klick innerhalb des Tabs „Layout“ auf „Assign unique IDs [...]“ benennt die IDs entsprechend der Readingorder um.

In Transkribus gibt es eine Fülle an unterschiedlichsten HTR-Modellen zur Handschriftenerkennung. Besonders der Zeitraum des 18. und 19. Jahrhunderts ist dabei gut abgedeckt. Naturgemäß ähneln sich zwar die Stile der Kurrentschrift unterschiedlicher „Hände“, bedürfen aber nichtsdestotrotz, insbesondere bei „krakeliger“ und untrainierter Handschrift, einer Nachbearbeitung.

Nach der vollständigen Layouterfassung und Transkription wurden die erste Annotation für die spätere Ausgabe im (TEI-)XML vorgenommen. Transkribus verfügt über ein bereits angelegtes Set an Tags, NutzerInnen können sich aber auch ihr Tagset selbst zusammenstellen und mit einer entsprechenden Tastenkombination anwenden (ALT+x).

Für das Friedhofsregister wurde die standardmäßige Annotation wie `<persName>`, `<date>`, `<placeName>` etc. vorgenommen.

![Ansicht des XML-Taggings in Transkribus](https://i.imgur.com/JDdIsr7.png)

Jeder Sterbe- bzw. Beerdigungseintrag hat eine Nummer. Im anhängenden alphabetischen Register lassen sich diese Nummern wiederfinden. Damit eine spätere Verknüpfung von Name bzw. Nummer im Register und dem eigentlichen Sterbeeintrag vorbereitet werden konnte, wurde jeder Nummer eines Eintrags ein `<label>`, und analog dazu den Nummern im alphabetischen Register ein `<ref>` zugewiesen.

Das nun komplette und annotierte Dokument wurde schließlich in page-XML und ALTO exportiert.

<h2 id="postprocessing">Postprocessing – der Weg zum TEI</h2>

Da am Ende zwei Ergebnisse stehen sollten, „trennen“ sich hier die Wege der Nachbearbeitung. Für die Ansicht im DFG-Viewer stehen die Formate ALTO und METS nebeneinander – sie spielen in diesem Schritt keine Rolle mehr. Für die volle Nutzbarkeit der Annotationen innerhalb des XML/TEI wird jedoch das DTA verwendet. Hierzu wird ein valides TEI gemäß des DTA-Basisformats benötigt<sup id="a11">[11](#f11)</sup>. Aus den exportierten page-XMLs aus Transkribus wurde nun ein zusammenhängendes TEI geschaffen. Mittels page2tei<sup id="a12">[12](#f12)</sup> lässt sich das relativ einfach realisieren. Neben dem verfügbaren Paket auf GitHub wird noch der XSLT- und XQuery-Prozessor *Saxon* zur Transformation benötigt<sup id="a13">[13](#f13)</sup>. Exportiert man aus Transkribus die page-XML- und METS-Dateien kann dann folgender Befehl ausgeführt werden:

    $ java -jar saxon9he.jar -xsl:page2tei-0.xsl -s:mets.xml -o:friedhofsregister_strelitz.xml

Nun ist ein zusammenhängendes TEI aus den page-XML-Dateien generiert worden.  

Zuerst wurde eine Unterteilung des Registers vorgenommen. Die Seiten 1 bis 65 sind Sterbeeinträge, die Seiten 66 bis 96 bilden das alphabetische Register. Gemäß des DTA-Basisformats wurden diese beiden Einheiten mittels `<div>` umschlossen, wobei das alphabetische Register noch um das Attribut `@type=”index”` erweitert wurde. Der Inhalt der beiden Abschnitte wurde mittels `<head>` ausgezeichnet<sup id="a14">[14](#f14)</sup>.

Da jeder Eintrag mit einer Textregion und damit einem `<p>` umkapselt ist, wurde von jedem beginnenden bis endenden `<p>`, das Tag `<item>`<sup id="a15">[15](#f15)</sup> umschlossen. Das Umschließen mit dem Tag <item> konnte erst in diesem Schritt, und nicht in Transkribus selber, vorgenommen werden. Transkribus hat nämlich den Nachteil, dass sobald mehrere aufeinanderfolgende Zeilen markiert und dann annotiert werden, das jeweilige Tag bei jeder Zeile neu beginnt und schließt:

~~~ xml
<persName>Esther Hirsch</persName></lb>
<persName>gb. Jacob</persName>
~~~

Für die Wohlgeformheit des TEI sollte jedoch ein Tag, in diesem Fall das Tag `<persName>`, auch trotz Zeilenumbruch einmal umschließend gesetzt werden. Daher wurde im Nachgang mit regulären Ausdrücken gearbeitet<sup id="a16">[16](#f16)</sup>. In diesem Beispiel:

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

Einem `<item>` wurde nun eine genaue xml:id zugewiesen, die sich aus dem Tag `<label>` innerhalb eines `<item>` ergibt. Ein dafür angefertigtes Perl-Skript<sup id="a17">[17](#f17)</sup> liest in jedem Eltern-Element `<item>` das Kind-Element `<label>` aus und weist die entsprechende Nummer als `xml:id` zu. Das Perl-Skript ignoriert dabei die inkonsequente Nummerierung im Friedhofsregister wie bspw. „No 1” vs „1” und generiert die xml:id nur aus den numerischen Werten. Da eine xml:id keine Ziffern an erster Stelle haben darf, wurde der xml:id ein Buchstabe vorangestellt. Damit sind nun `<ref>` und `<item>` genau miteinander verbunden.

Da alle Einträge einem Listenschema folgen, wurden sie vollständig mit dem Tag `<list>` umschlossen, die Paginierung auf jeder einzelnen Seite mit einem `<fw>`. Da sich die Paginierung immer oben befindet und als Folierungsnummer dient, wurden `<fw>` um die Attributwerte `@place="top"` und `@type="folNum"` erweitert.

Die Personenname und das damit verbundene Tag `<persName>` wurde, sofern sinnvoll und möglich, mit dem Attribut `@ref` erweitert. Als ref-Wert wurde eine standardmäßige Verlinkung zur entsprechenden GND<sup id="a18">[18](#f18)</sup> verwendet. Für den ref-Wert des `</placeName>` wurde GeoNames<sup id="a19">[19](#f19)</sup> genutzt.

  

Einige Beerdigungseinträge führen auch den Beruf oder Funktion innerhalb der Gemeinde auf. Da `<occupation>` innerhalb von `<item>` nicht zulässig ist und in vielen Fällen wie „Gemeindediener“, „Rabbi“ oder „Ältester“ auch nicht passend erscheint, wurden diese Bezeichnungen mit `<roleName>` ausgezeichnet.

Die hebräischen Anmerkungen wurden mittels `<foreign>` und dem Attributwert `@xml:lang="hbo">`<sup id="a20">[20](#f20)</sup> umschlossen.

Letztlich wurde noch der TEI-Header gemäß des DTABfs angepasst und einige Metadaten, wie etwa <repository> für das besitzende Instituts der Vorlage oder <author> für den Herausgeber des Registers, angepasst.

<h2 id="mets">Generierung der METS aus ALTO</h2>

Die Formate ALTO und METS stehen parallel nebeneinander. Die einzelnen ALTO-XMLs konnten wie bereits im vorherigen Abschnitt beschrieben, aus Transkribus exportiert werden. ALTO enthält im XML Schema alle verfügbaren Daten des Layouts der zugrundeliegenden Vorlage.

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

die METS-Datei wurde wurde mittels *tei2mets*<sup id="a21">[21](#f21)</sup> generiert. In ihr befinden sich alle relevanten Metadaten über das Friedhofsregister.

Nun sind durch die Formate ALTO und METS der transkribierte Text exakt mit den Bildigitalisaten verbunden. Im DFG-Viewer lässt sich das Ergebnis anschauen; die „Maschine“ weiß also, welche Textregion und welche Textzeile zu welcher Position innerhalb des Bildes gehört.

Unter www lässt sich nun das Register samt Volltext im DFG-Viewer betrachten.

<h2 id="ausblick">Ausblick</h2>

Innerhalb des Friedhofregisters lassen sich einige verwandtschaftlichen Beziehungen aufdecken. Welches Tag dafür?

Datumsangaben sind bisher lediglich mit `<date>` umschlossen, eine Erweiterung um das Attribut `@when` wäre zur maschinellen Verarbeitung der Daten denkbar. Dabei folgt die Angabe des Datums dem Schema `YY-MM-DD`, also bspw:  
~~~xml
<date when="1822-11-02">2t Novbr 1822</date>
~~~
  
Auch eine Auszeichnung mit dem Tag `<death>` und dem Attribut `@when` ist möglich. In einigen Fällen ist auch das Geburtsdatum angegeben, diese könnten dann analog durch `<birth>` und `@when` ausgezeichnet werden.
***

<b id="f1">1</b> siehe [www.deutschestextarchiv.de](www.deutschestextarchiv.de) [↩](#a1)

<b id="f2">2</b> vgl. Donath, Leopold: Geschichte der Juden in Mecklenburg von den ältesten Zeiten (1266) bis auf die Gegenwart (1874), Leipzig: Verlag Oskar Leiner 1874, S. 138. [Online verfügbar GoogleBooks.](https://books.google.de/books?id=JnRhAAAAcAAJ&pg=PA138) [↩](#a2)

<b id="f3">3</b> vgl. Tychsen, Oluf Gerhard: Bützowische Nebenstunden. Dritter Theil, Bützow 1768, S.5. [Online verfügbar Rostocker Dokumentenserver.](http://rosdok.uni-rostock.de/resolve/id/rosdok_document_0000016029)  [↩](#a3)

<b id="f4">4</b> Landeshauptarchiv Schwerin: 4.11-16 Judenangelegenheiten (Acta judaeorum) Mecklenburg-Strelitz, Nr. 271. [↩](#a4)

<b id="f5">5</b> vgl. Donath, Leopold: Geschichte der Juden in Mecklenburg von den ältesten Zeiten (1266) bis auf die Gegenwart (1874), Leipzig: Verlag Oskar Leiner 1874, S. 139. [Online verfügbar GoogleBooks.](https://books.google.de/books?id=JnRhAAAAcAAJ&pg=PA139) Für eine ausführliche Geschichte zur jüdische Gemeinde zu Strelitz siehe den Abschnitt [Neustrelitz](http://www.juden-in-mecklenburg.de/Orte/Neustrelitz) unter „Juden in Mecklenburg“ von Jürgen Gramenz und Sylvia Ulmer. [↩](#a5)

<b id="f6">6</b> Zur ausführlichen Geschichte des Friedhofs vgl. [„Jüdischer Friedhof Alt-Strelitz”](http://www.juden-in-mecklenburg.de/Friedhoefe/Juedischer_Friedhof_Alt_Strelitz) unter „Juden in Mecklenburg“ von Jürgen Gramenz und Sylvia Ulmer. [↩](#a6)

<b id="f7">7</b> Die Seelenregister, analog etwa zu Kirchenbüchern, der jüdischen Gemeinde zu Strelitz sind bisher als Gesamtbestand nicht gefunden worden. Weder im Landeshauptarchiv in Schwerin, noch in den Beständen des historischen Archiv der Stiftung Neue Synagoge Berlin – Centrum Judaicum noch im Central Archives for the History of the Jewish People Jerusalem (CAHJP). Laut [familysearch.org](https://www.familysearch.org/de/), einer Seite für Familienforschung betrieben von der „Kirche Jesu Christi der Heiligen der Letzten Tage“, die in Deutschland und ganz Europa unzählige Kirchenbücher mikroverfilmt hat, gibt es auch für die jüdische Gemeinde mikroverfilmte Matrikel. Allerdings lässt die Bezeichnung des Mikrofilms mit der Nummer 1185018 *Tote & Index 1760-1923 Grabinschriften ca. 1820-1888* schon darauf schließen, dass es sich, jedenfalls was das Register und den Index betrifft, ebenfalls um Jacobsons Abschrift handelt. Die Grabinschriften sind vermutlich die in Hebräisch geschriebenen Anmerkung unter dem Namen und dem Sterbetag im Register. Die Mikrofilme sind jedoch nur in der Family History Library in Salt Lake City einsehbar und können nicht (mehr) ausgeliehen bzw. bestellt werden. Als letzter dienlicher Hinweis sei hier noch genannt, dass Leopold Donath in seinem bereits zitierten Werk zur Geschichte der Juden in Mecklenburg vermerkt, dass der damalige Landesrabbiner Jacob Hamburger ihm Auskunft aus dem „Gedenkbuch des dortigen Beerdigungsvereins“ gab – aber auch dieses Gedenkbuch konnte bisher nicht ausfindig gemacht werden.h [↩](#a7)

<b id="f8">8</b>Altstrelitz, cemetery register, photocopy, German and Hebrew, 1740-1923, Box: 7, Folder: III2. Jacob Jacobson Collection, AR 7002 / MF 447 / MF 134. Leo Baeck Institute. [https://archives.cjh.org/repositories/5/archival_objects/330811](https://archives.cjh.org/repositories/5/archival_objects/330811). [↩](#a8)

<b id="f9">9</b> Als ausgezeichnete Metasuchmaschine für Archivalien deutsch-jüdischen Ursprungs eignet sich die Datenbank vom Center for Jewish History, [https://www.cjh.org/](https://www.cjh.org/), hierüber lassen sich Archivalien, welche auch im großen Umfang bereits digitalisiert wurden, auffinden. Bei der Recherche sind die Bestände der Nationalbibliothek von Israel, [https://web.nli.org.il](https://web.nli.org.il), von ebenso großer Bedeutung, ebenso wie das Central Archives for the History of the Jewish People (CAHJP), [http://cahjp.nli.org.il/](http://cahjp.nli.org.il/), welches zum größten Teil die (Teil-)Nachlässe jüdischer Gemeinde in Deutschland verwahrt.  [↩](#a9)

<b id="f10">10</b> Zum Trainieren eigener Layouterkennungs-Modelle eignet sich das Tool [P2PaLA](https://github.com/lquirosd/P2PaLA); eine Einbettung in die Software Transkribus hat bereits stattgefunden und wird laufend ausgebaut. [↩](#a10)

<b id="f11">11</b> siehe dazu die Dokumentation des DTABfs unter [http://www.deutschestextarchiv.de/doku/basisformat/](http://www.deutschestextarchiv.de/doku/basisformat/). [↩](#a11)

<b id="f12">12</b> [https://github.com/dariok/page2tei](https://github.com/dariok/page2tei). [↩](#a12)

<b id="f13">13</b> [https://www.saxonica.com](https://www.saxonica.com). [↩](#a13)

<b id="f14">14</b> siehe dazu auch den Abschnitt *Texteinteilung auf Kapitelebene* unter [http://www.deutschestextarchiv.de/doku/basisformat/div.html](http://www.deutschestextarchiv.de/doku/basisformat/div.html). [↩](#a14)

<b id="f15">15</b> siehe hierzu auch die Empfehlungen der TEI unter [https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-item.html](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-item.html). [↩](#a15)

<b id="f16">16</b> Um reguläre Ausdrücke zu testen bzw. zu erstellen, eignet sich die Webanwendung *regex101* ausgezeichnet, siehe [https://regex101.com](https://regex101.com). [↩](#a16)

<b id="f17">17</b> Das Skript wurde von Frank Wiegand geschrieben und findet sich auf GitHub, [https://gist.github.com/haoess/77e1eda37fa18fe764d76dbc7b4e9240](https://gist.github.com/haoess/77e1eda37fa18fe764d76dbc7b4e9240). [↩](#a17)

<b id="f18">18</b> Gemeinsame Normdatei, siehe [https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html](https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html). [↩](#a18)

<b id="f19">19</b> siehe [https://www.geonames.org](https://www.geonames.org). [↩](#a19)

<b id="f20">20</b> Der Wert für fremdsprachliches Material ist das Kürzel internationale Norm ISO 639-3, in diesem Fall handelt es sich um rabbinisches Hebräisch. [↩](#a20)

<b id="f21">21</b> siehe dazu [https://github.com/tboenig/tei2mets](https://github.com/tboenig/tei2mets) von Matthias Boenig [↩](#a21)
