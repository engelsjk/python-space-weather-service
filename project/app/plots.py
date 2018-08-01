"""
plots.py
Create plot! 
"""

import numpy as np
import pandas as pd
from plotnine import * 
from mizani.formatters import date_format
import warnings 

##############################################
# Plotter

class Plotter:

    height = 0
    width = 12

    titles_by_signal={
        'P1': '>= 1 MeV Proton Flux (5-Minute Data)',
        'P5': '>= 5 MeV Proton Flux (5-Minute Data)',
        'P10': '>= 10 MeV Proton Flux (5-Minute Data)',
        'P50': '>= 50 MeV Proton Flux (5-Minute Data)',
        'P100': '>= 100 MeV Proton Flux (5-Minute Data)'
    }

    unknown_title = 'Unknown Signal (5-Minute Data)'

    def __init__( self ):
        pass

    def set_height_width( self, height, width ):
        self.height = height 
        self.width = width

    def enable_warning_filter( self ):
        """Disable warnings from plotnine lib."""
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)

    def create_plot( self, data, meta ):
        """Create plot w/ custom stylings."""
        print(meta)
        title_by_signal = self.titles_by_signal.get( meta['signal'], self.unknown_title )
        title_by_signal += "\n Data Source: %s" % meta['source']

        ###

        x = np.array( data['values'] )
        x = x.astype( np.float )
        t = np.array( data['time'] )

        d = { 'values': x, 'time': t }
        df = pd.DataFrame( data=d )
        df['time'] = pd.to_datetime( df['time'] )

        ###

        t0 = df['time'][0]

        plot_theme = theme(
            figure_size=( self.height, self.width ),
            panel_background=element_rect( fill="black" ),
            plot_background=element_rect( fill="gray" ),
            panel_grid_major_y=element_blank(),
            panel_grid_major_x=element_blank(),
            panel_grid_minor_y=element_blank(),
            panel_grid_minor_x=element_blank(),
            title=element_text( color="black",size=20 ),
            axis_text_x=element_text( color="black",size=10 ),
            axis_text_y=element_text( color="black",size=15 ),
            axis_title_x=element_text( color="black",size=12 ),
            axis_title_y=element_text( color="black",size=15 ),
        )

        g = (ggplot()
            + geom_line( df, aes( 'time','values' ), color="#76D115", size=2 )
            + scale_x_datetime( labels = date_format( "%b %d %H:%M" ) )
            + ggtitle( title_by_signal ) 
            + xlab( "Universal Time" )  
            + ylab( "Proton Flux Unit : Particles $cm^{-2}s^{-1}sr^{-1}$" )
            + plot_theme 
        )

        if meta['signal'] == 'P10':
            g = ( g + ylim ( 10**-1, 10**4 )
            + scale_y_log10( breaks=[10**-1, 10**0, 10**1, 10**2, 10**3, 10**4] ) 
            + geom_hline( yintercept=10**0, color="#E6C329", size=3 )
            + annotate( geom="text", label="WARNING", x=t0 , y=1.15*10**0, ha="left", size=12, color = "#E6C329" )
            + geom_hline( yintercept=10**1, color="#DE7F12", size=3 )
            + annotate( geom="text", label="ALERT", x=t0 , y=1.15*10**1, ha="left", size=12, color = "#DE7F12" )
            + geom_hline( yintercept=10**2, color="#B52914", size=3 )
            + annotate( geom="text", label="CRITICAL", x=t0 , y=1.15*10**2, ha="left", size=12, color = "#B52914" )
        )

        return g
