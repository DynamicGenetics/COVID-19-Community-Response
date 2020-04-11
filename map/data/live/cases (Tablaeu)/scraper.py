import tableauserverclient as TSC

tableau_auth = TSC.TableauAuth('chris.moreno-stokoe@bristol.ac.uk', 'gGSgX.ii47V$RkV', 'en-gb/gallery/gardeners-planting-guide?tab=viz-of-the-day&type=viz-of-the-day')
server = TSC.Server('https://public.tableau.com/')



with server.auth.sign_in(tableau_auth):
    all_datasources, pagination_item = server.datasources.get()
    print("\nThere are {} datasources on site: ".format(pagination_item.total_available))
    print([datasource.name for datasource in all_datasources])