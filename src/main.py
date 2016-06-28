# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:19:28 2016

@author: loic
"""


if __name__ == "__main__":
    import server
    import threads
    
    threads.launch_thread()
    server.launchServer()
    threads.launch_thread()

    print "Starting server"
#    app.run(debug=True, host='0.0.0.0')
    
    """ Running on C. Concolato's files"""
    print "Server launched"
#    import PDFdl
#    PDFdl.downloadAll(data+os.sep+"concolato.bib")