# MKV Fixes

#### Python CGI frontend to run [**mkclean tool**](http://www.matroska.org/downloads/mkclean.html) on the MKV's found on the dir

Just insert the DIR to scan and a bootstrap _html_ will show you a list of candidates, with a **Fix** button

	* Using [_Python Cheetah_](http://www.cheetahtemplate.org/) templates
	* Twitter bootstrap


#### You can customize (and even password protect your CGI dir)

>	sudo vim /etc/apache2/conf-enabled/serve-cgi-bin.conf

And add the **AuthType basic**

        <IfDefine ENALBLE_USR_LIB_CGI_BIN>
                ScriptAlias /cgi-bin/ /var/www/cgi-bin/
                <Directory "/var/www/cgi-bin">
                        AuthType basic
                        AuthName "CGI stuff"
                        AuthUserFile /etc/users
                        Require valid-user
                        AllowOverride None
                        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
                </Directory>
        </IfDefine>