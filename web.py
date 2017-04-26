import http.server
import http.client
import json

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    OPENFDA_API_URL= "api.fda.gov"
    OPENFDA_API_EVENT= "/drug/event.json"

    def get_event(self,limit=10):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit="+str(limit))
        r1= conn.getresponse()
        leer= r1.read()
        leer1= leer.decode("utf8")

        event= json.loads(leer1)
        return event

    def get_events_search_companies(self):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
        drug= self.path.split("=")[1]
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10&search=companynumb:"+drug)
        r1= conn.getresponse()
        leer= r1.read()
        leer1= leer.decode("utf8")

        events= json.loads(leer1)
        return events


    def get_medicamentos_from_events(self,events):
        medicamentos=[]
        for i in events:
            medicamentos+=[i["patient"]["drug"][0]["medicinalproduct"]]
        return medicamentos

    def get_medicamentos_html(self, medicamentos):
        html3= """
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <ol>
        """

        for i in medicamentos:
            html3 += "<li>" + i + "</li>\n"

        html3 += """
                </ol>
            </body>
        </html>
        """
        return html3

    def get_events_search_medicamentos(self):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
        drug= self.path.split("=")[1]
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10&search=patient.drug.medicinalproduct:"+drug)
        r1= conn.getresponse()
        leer= r1.read()
        leer1= leer.decode("utf8")

        events= json.loads(leer1)
        return events

    def get_companies_from_events(self,events):
        companies=[]
        for i in events:
            companies+=[i["companynumb"]]
        return companies

    def get_companies_html(self, companies):
        html4= """
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <ol>
        """

        for i in companies:
            html4 += "<li>" + i + "</li>\n"

        html4 += """
                </ol>
            </body>
        </html>
        """
        return html4

    def get_main_page(self):
        html="""
        <html>
            <head>
                <title>OpenF07DA Cool App</title>
            </head>

            <body>
            <font size=6>
            <body style= "background-color:#C48DAC">
            <span style="color:#47111F">
                <h1>OpenFDA Client</h1>
                <form method="get" action="listDrugs">
                    <input type= "submit" value="Lista medicamentos">
                    </input>

                    <input type= "text" name="Limit">
                    </input>
                </form>

                <form method= "get" action="searchDrug">
                    <input type="text" name="drug">
                    </input>

                    <input type="submit" value="Buscar medicamentos">
                    </input>
                </form>

                <form method="get" action="listCompanies">
                    <input type= "submit" value="Lista companias">
                    </input>

                    <input type= "text" name="Limit">
                    </input>
                </form>

                <form method= "get" action="searchCompany">
                    <input type="text" name="company">
                    </input>
                    <input type="submit" value="Buscar companias">
                    </input>
                </form>

                <form method= "get" action="listGender">
                    <input type="submit" value="Generos pacientes">
                    </input>

                    <input type= "text" name="Limit">
                    </input>
                </form>
            </font>
            </body>
        </html>
        """
        return html

    def get_list_html(self, drugs):
        html2= """
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <ol>
        """

        for drug in drugs:
            html2 += "<li>" + drug + "</li>\n"

        html2 += """
                </ol>
            </body>
        </html>
        """
        return html2

    def get_notfound_html():
        html="""
        <html>
            <head>
                <title>ERROR 404 not found</title>
            </head>
            <body>
                <form method="get" action="not_exists_resource">
            </body>
        </html>
        """
        return html

    def get_secret_html():
        html="""
        <html>
            <head>
                <title>CODIGO 401 Unauthorized</title>
            </head>
            <body>
                <form method="get" action="secret">
            </body>
        </html>
        """
        return html

    def get_redirect_html():
        html="""
        <html>
            <head>
                <title>redirect</title>
            </head>
            <body>
                <form method="get" action="redirect">
            </body>
        </html>
        """
        return html

    def do_GET(self):
        main_page= False
        is_event_drugs=False
        is_event_companies=False
        is_search_drugs=False
        is_search_companies=False
        patientsex=False
        test_not_found=False
        test_auth=False
        test_redirect=False


        if self.path== "/": #cuando ponga una barra el cliente en la parte de arriba mostrar la pagina principal
            main_page= True
        elif "listDrugs" in self.path:
            is_event_drugs= True
        elif "listCompanies" in self.path:
            is_event_companies= True
        elif "searchCompany" in self.path:
            is_search_drugs=True
        elif "searchDrug" in self.path:
            is_search_companies=True
        elif "listGender" in self.path:
            patientsex=True
        elif "not_exists_resource" in self.path:
            test_not_found=True
        elif "secret" in self.path:
            test_auth=True
        elif "redirect" in self.path:
            test_redirect=True


        if test_not_found==True:
            self.send_response(404)
            self.send_header("Content-type","text/html")
            self.end_headers()
            html= self.get_notfound_html()

        if test_auth==True:
            self.send_response(401)
            self.send_header("WWW-Authenticate","basic Realm")
            self.end_headers()
            html=self.get_secret_html()

        if test_redirect==True:
            self.send_response(302)
            self.send_header("Location","http://localhost:8000/")
            self.end_headers()
            html=self.get_redirect_html()

        else:
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            html= self.get_main_page()



        if main_page:
            self.wfile.write(bytes(html,"utf8")) #wfile fichero de escritura que esta enganchado con el cliente, aqui dentro de este fichero
                                                 #ponemos el codigo html
        elif is_event_companies:
            limit= self.path.split("=")[1]
            if limit=="":
                limit=10

            events= self.get_event(str(limit))
            results= events["results"]
            drugs=[]
            for i in results:
                drug= i["companynumb"]
                drugs+= [drug]


            html2= self.get_list_html(drugs)

            self.wfile.write(bytes(html2,"utf8")) #en este caso le mandamos la informacion dentro de webserver

        elif is_event_drugs:
            limit= self.path.split("=")[1]
            if limit=="":
                limit=10

            events= self.get_event(str(limit))
            results= events["results"]
            drugs=[]
            for i in results:
                drug= i["patient"]["drug"][0]["medicinalproduct"]
                drugs+= [drug]


            html2= self.get_list_html(drugs)

            self.wfile.write(bytes(html2,"utf8"))

        elif is_search_companies:
            events= self.get_events_search_medicamentos()
            results=events["results"]
            companies= self.get_companies_from_events(results)

            html3= self.get_companies_html(companies)

            self.wfile.write(bytes(html3, "utf8"))

        elif is_search_drugs:
            events= self.get_events_search_companies()
            results=events["results"]
            drugs= self.get_medicamentos_from_events(results)

            html4= self.get_medicamentos_html(drugs)

            self.wfile.write(bytes(html4, "utf8"))

        elif patientsex:
            limit= self.path.split("=")[1]
            if limit=="":
                limit=10
            events= self.get_event(str(limit))
            results= events["results"]
            drugs=[]
            for i in results:
                drug= i["patient"]["patientsex"]
                drugs+= [drug]
            html2= self.get_list_html(drugs)

            self.wfile.write(bytes(html2,"utf8"))



        return
