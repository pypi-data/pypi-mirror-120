# fetch_files tab for bfit
# Derek Fujimoto
# Nov 2017

from tkinter import *
from tkinter import ttk, messagebox, filedialog
from bfit import logger_name
from bdata import bdata, bmerged
from functools import partial
from bfit.backend.fitdata import fitdata
from bfit.gui.popup_prepare_data import popup_prepare_data
from bfit.backend.entry_color_set import on_focusout, on_entry_click
import bfit.backend.colors as colors
from bfit.global_variables import KEYVARS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time, datetime, os, logging, glob, re

__doc__="""
    """

# =========================================================================== #
# =========================================================================== #
class fetch_files(object):
    """
        Data fields:
            
            asym_type: StringVar, drawing style
            bfit: pointer to parent class
            base_bins = IntVar, number of bins to use as baseline on scan ends
            canvas_frame_id: id number of frame in canvas
            check_rebin: IntVar for handling rebin aspect of checkall
            check_bin_remove: StringVar for handing omission of 1F data
            check_state: BooleanVar for handling check all
            check_state_data: BooleanVar for handling check_all_data
            check_state_fit: BooleanVar for handling check_all_fit
            check_state_res: BooleanVar for handling check_all_res
            data_canvas: canvas object allowing for scrolling 
            dataline_frame: frame holding all the data lines. Exists as a window
                in the data_canvas
            data_lines: dictionary of dataline obj, keyed by run number
            data_lines_old: dictionary of removed dataline obj, keyed by run number
            entry_asym_type: combobox for asym calc and draw type
            entry_run: entry to put in run number string
            fet_entry_frame: frame of fetch tab
            filter_opt: StringVar, holds state of filter radio buttons
            listbox_history: listbox for run input history
            max_number_fetched: max number of files you can fetch
            omit_state: BooleanVar, if true set omit all final incomplete scans
            run: StringVar input to fetch runs.
            runmode_label: display run mode
            runmode: display run mode list of strings
            text_filter: Text box for filter commands input
            year: IntVar of year to fetch runs from 
    """
    
    runmode_relabel = {'20':'SLR (20)', 
                       '1f':'Frequency Scan (1f/1x)', 
                       '1x':'Frequency Scan (1f/1x)', 
                       '1w':'Frequency Comb (1w)', 
                       '2e':'Random Freq. (2e)', 
                       '1n':'Rb Cell Scan (1n)', 
                       '1e':'Field Scan (1e)', 
                       '2h':'Alpha Tagged (2h)'}
                       
    equivalent_modes = [['1f', '1x'], ['20', '2h']]
                       
    run_number_starter_line = '40001 40002+40003 40005-40010 (run numbers)'
    bin_remove_starter_line = '24 100-200 (bins)'
    max_number_fetched = 500
    nhistory = 10
    
    # ======================================================================= #
    def __init__(self, fetch_data_tab, bfit):
        
        # get logger
        self.logger = logging.getLogger(logger_name)
        self.logger.debug('Initializing')
    
        # initialize
        self.bfit = bfit
        self.data_lines = {}
        self.data_lines_old = {}
        self.fit_input_tabs = {}
        self.check_rebin = IntVar()
        self.check_bin_remove = StringVar()
        self.check_state = BooleanVar()
        self.fetch_data_tab = fetch_data_tab
        
        # Frame for specifying files -----------------------------------------
        fet_entry_frame = ttk.Labelframe(fetch_data_tab, text='Specify Files')
        self.year = IntVar()
        self.run = StringVar()
        
        self.year.set(self.bfit.get_latest_year())
        
        entry_year = Spinbox(fet_entry_frame, textvariable=self.year, width=5, 
                             from_=2000, to=datetime.datetime.today().year)
        entry_run = Entry(fet_entry_frame, textvariable=self.run, width=100)
        entry_run.insert(0, self.run_number_starter_line)
        entry_run.config(foreground=colors.entry_grey)
        
        # history list
        self.listbox_history = Listbox(fetch_data_tab, selectmode=SINGLE)
        entry_fn = partial(on_entry_click, text=self.run_number_starter_line, \
                            entry=entry_run)
        on_focusout_fn = partial(on_focusout, text=self.run_number_starter_line, \
                            entry=entry_run)
        entry_run.bind('<FocusIn>', entry_fn)
        entry_run.bind('<FocusOut>', on_focusout_fn)
        entry_run.bind('<Leave>', lambda event: self.history_hide(event, 'entry'))
        
        entry_run.bind('<Enter>', self.history_show)
        self.listbox_history.bind('<Leave>', lambda event: self.history_hide(event, 'history'))
        self.listbox_history.bind("<<ListboxSelect>>", self.history_set)
        
        # fetch button
        fetch = ttk.Button(fet_entry_frame, text='Fetch', command=self.get_data)
        
        # grid and labels
        fet_entry_frame.grid(column=0, row=0, sticky=(N, W, E), columnspan=2, padx=5, pady=5)
        ttk.Label(fet_entry_frame, text="Year:").grid(column=0, row=0, sticky=W)
        entry_year.grid(column=1, row=0, sticky=(W))
        ttk.Label(fet_entry_frame, text="Run Number:").grid(column=2, row=0, sticky=W)
        entry_run.grid(column=3, row=0, sticky=W)
        fetch.grid(column=4, row=0, sticky=E)
        self.listbox_history.grid(column=3, row=1, sticky=W)
        
        # padding 
        for child in fet_entry_frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        
        self.listbox_history.grid_forget()
        
        # Frame for run mode -------------------------------------------------
        runmode_label_frame = ttk.Labelframe(fetch_data_tab, pad=(10, 5, 10, 5), \
                text='Run Mode', )
        
        self.runmode_label = ttk.Label(runmode_label_frame, text="", justify=CENTER)
        
        # Scrolling frame to hold datalines
        yscrollbar = ttk.Scrollbar(fetch_data_tab, orient=VERTICAL)         
        self.data_canvas = Canvas(fetch_data_tab, bd=0,              # make a canvas for scrolling
                yscrollcommand=yscrollbar.set,                      # scroll command receive
                scrollregion=(0, 0, 5000, 5000), confine=True)       # default size
        yscrollbar.config(command=self.data_canvas.yview)           # scroll command send
        dataline_frame = ttk.Frame(self.data_canvas, pad=5)          # holds 
        
        self.canvas_frame_id = self.data_canvas.create_window((0, 0),    # make window which can scroll
                window=dataline_frame, 
                anchor='nw')
        dataline_frame.bind("<Configure>", self.config_canvas) # bind resize to alter scrollable region
        self.data_canvas.bind("<Configure>", self.config_dataline_frame) # bind resize to change size of contained frame
        
        
        
        # Frame to hold everything on the right ------------------------------
        bigright_frame = ttk.Frame(fetch_data_tab, pad=5)
        
        # asymmetry calculation
        style_frame = ttk.Labelframe(bigright_frame, text='Asymmetry Calculation', \
                pad=5)
        self.asym_type = StringVar()
        self.asym_type.set('')
        self.entry_asym_type = ttk.Combobox(style_frame, \
                textvariable=self.asym_type, state='readonly', \
                width=20)
        self.entry_asym_type['values'] = ()
        
        style_frame.grid(column=0, row=0, sticky=(W, N, E))
        style_frame.grid_columnconfigure(0, weight=1)
        self.entry_asym_type.grid(column=0, row=0, sticky=(N, E, W), padx=10)
        
        # Frame for group set options ----------------------------------------
        right_frame = ttk.Labelframe(bigright_frame, \
                text='Operations on Active Items', pad=15)
        
        check_remove = ttk.Button(right_frame, text='Remove', \
                command=self.remove_all, pad=5)
        check_draw = ttk.Button(right_frame, text='Draw', \
                command=lambda:self.draw_all('data'), pad=5)
        
        
        # Scan repair options ------------------------------------------------
        frame_scan = ttk.Labelframe(right_frame, \
                text='Scan Repair Options', pad=5)
        
        check_rebin_label = ttk.Label(frame_scan, text="Rebin:", pad=5)
        check_rebin_box = Spinbox(frame_scan, from_=1, to=100, width=3, \
                textvariable=self.check_rebin, 
                command=lambda: self.set_all('rebin'))
        
        check_bin_remove_label = ttk.Label(frame_scan, text="Remove:", pad=5)
        check_bin_remove_entry = Entry(frame_scan, \
                textvariable=self.check_bin_remove, width=20)
        
        self.omit_state = BooleanVar()
        omit_checkbox = ttk.Checkbutton(frame_scan, 
                text='Omit incomplete final scan', variable=self.omit_state, 
                onvalue=True, offvalue=False, pad=5, 
                command=lambda: self.set_all('omit_scan'))
        self.omit_state.set(False)
        
        self.base_bins = IntVar()
        base_label = ttk.Label(frame_scan, text="baseline bins", pad=5)
        base_spinbox = Spinbox(frame_scan, from_=0, to=1000, width=4, \
                               textvariable=self.base_bins, 
                               command=lambda: self.set_all('base_bins'))
        self.base_bins.set(0)
        
        # grid
        check_rebin_label.grid(     column=0, row=0, sticky='e')
        check_rebin_box.grid(       column=1, row=0, sticky='w')
        check_bin_remove_label.grid(column=0, row=1, sticky='e')
        check_bin_remove_entry.grid(column=1, row=1, sticky='w', columnspan=2)
        omit_checkbox.grid(column=0, row=2, sticky='w', columnspan=2)
        base_spinbox.grid(column=0, row=3, sticky='e')
        base_label.grid(column=1, row=3, sticky='w')
        
        # key bindings
        check_bin_remove_entry.bind('<KeyRelease>', lambda x: self.set_all('omit'))
        check_rebin_box.bind('<KeyRelease>', lambda x: self.set_all('rebin'))
        base_spinbox.bind('<KeyRelease>', lambda x: self.set_all('base_bins'))
        
        # checkboxes
        right_checkbox_frame = ttk.Frame(right_frame)
        
        check_all_box = ttk.Checkbutton(right_checkbox_frame, 
                text='State', variable=self.check_state, 
                onvalue=True, offvalue=False, pad=5, command=self.check_all)
        self.check_state.set(True)
        
        self.check_state_data = BooleanVar()        
        check_data_box = ttk.Checkbutton(right_checkbox_frame, 
                text='Data', variable=self.check_state_data, 
                onvalue=True, offvalue=False, pad=5, command=self.check_all_data)
        self.check_state_data.set(True)
        
        self.check_state_fit = BooleanVar()        
        check_fit_box = ttk.Checkbutton(right_checkbox_frame, 
                text='Fit', variable=self.check_state_fit, 
                onvalue=True, offvalue=False, pad=5, command=self.check_all_fit)
        
        self.check_state_res = BooleanVar()        
        check_res_box = ttk.Checkbutton(right_checkbox_frame, 
                text='Res', variable=self.check_state_res, 
                onvalue=True, offvalue=False, pad=5, command=self.check_all_res)
                
        check_toggle_button = ttk.Button(right_frame, \
                text='Toggle All Check States', command=self.toggle_all, pad=5)
        
        # add grey to check_bin_remove_entry
        check_bin_remove_entry.insert(0, self.bin_remove_starter_line)
        
        check_entry_fn = partial(on_entry_click, \
                text=self.bin_remove_starter_line, \
                entry=check_bin_remove_entry)
        
        check_on_focusout_fn = partial(on_focusout, \
                text=self.bin_remove_starter_line, \
                entry=check_bin_remove_entry)
        
        check_bin_remove_entry.bind('<FocusIn>', check_entry_fn)
        check_bin_remove_entry.bind('<FocusOut>', check_on_focusout_fn)
        check_bin_remove_entry.config(foreground=colors.entry_grey)
                    
        # grid
        runmode_label_frame.grid(column=2, row=0, sticky=(N, W, E, S), pady=5, padx=5)
        self.runmode_label.grid(column=0, row=0, sticky=(N, W, E))
        
        bigright_frame.grid(column=2, row=1, rowspan=2, sticky='new')
        
        self.data_canvas.grid(column=0, row=1, sticky=(E, W, S, N), padx=5, pady=5)
        yscrollbar.grid(column=1, row=1, sticky=(W, S, N), pady=5)
        
        check_all_box.grid(        column=0, row=0, sticky=(N))
        check_data_box.grid(        column=1, row=0, sticky=(N))
        check_fit_box.grid(         column=2, row=0, sticky=(N))
        check_res_box.grid(         column=3, row=0, sticky=(N)) 
        
        right_frame.grid(           column=0, row=1, sticky=(N, E, W), pady=5)
        r = 0
        right_checkbox_frame.grid(  column=0, row=r, sticky=(N), columnspan=2); r+= 1
        check_toggle_button.grid(   column=0, row=r, sticky=(N, E, W), columnspan=2, pady=1, padx=5); r+= 1
        check_draw.grid(            column=0, row=r, sticky=(N, W, E), pady=5, padx=5);
        check_remove.grid(          column=1, row=r, sticky=(N, E, W), pady=5, padx=5); r+= 1
        frame_scan.grid(            column=0, row=r, sticky=(N, E, W), pady=5, padx=5, columnspan=2); r+= 1        
        
        # filtering -----------------------------------------------------------
        frame_filter = ttk.Labelframe(bigright_frame, text='Filter Runs', pad=5)
        button_filter_instr = ttk.Button(frame_filter, text='Instructions', 
                                         command=self.show_filter_instructions)
        self.text_filter = Text(frame_filter, width=35, height=5, state='normal', 
                                wrap='none')
        
        frame_filter_button = ttk.Frame(frame_filter, pad=5)
        button_filter = ttk.Button(frame_filter_button, text='Filter', 
                                         command=self.filter_runs)
        self.filter_opt = StringVar()
        self.filter_opt.set('activate')
        radio_filter_activate = ttk.Radiobutton(frame_filter_button, 
                                       variable=self.filter_opt, 
                                       value='activate',
                                       text='By activatation',
                                       )
        radio_filter_remove = ttk.Radiobutton(frame_filter_button, 
                                       variable=self.filter_opt, 
                                       value='remove',
                                       text='By removal',
                                       )
        
        button_filter.grid(column=0, row=0, rowspan=2, sticky='w', padx=5)
        radio_filter_activate.grid(column=1, row=0, sticky='w', padx=5)
        radio_filter_remove.grid(column=1, row=1, sticky='w', padx=5)
        
        # final grid
        frame_filter.grid(column=0, row=2, sticky='new', pady=5)
        r = 0
        button_filter_instr.grid(column=0, row=r, sticky='new', pady=5); r+= 1
        self.text_filter.grid(column=0, row=r, sticky='new', pady=5); r+= 1
        frame_filter_button.grid(column=0, row=r, sticky='new', pady=5); r+= 1
        
        # resizing
        fetch_data_tab.grid_columnconfigure(0, weight=1)        # main area
        fetch_data_tab.grid_rowconfigure(1, weight=1)            # main area
        
        for i in range(3):
            if i%2 == 0:    fet_entry_frame.grid_columnconfigure(i, weight=2)
        fet_entry_frame.grid_columnconfigure(3, weight=1)
            
        self.data_canvas.grid_columnconfigure(0, weight=1)    # fetch frame 
        self.data_canvas.grid_rowconfigure(0, weight=1)
            
        # passing
        self.entry_run = entry_run
        self.entry_year = entry_year
        self.check_rebin_box = check_rebin_box
        self.check_bin_remove_entry = check_bin_remove_entry
        self.check_all_box = check_all_box
        self.dataline_frame = dataline_frame

        self.logger.debug('Initialization success.')
    
    # ======================================================================= #
    def __del__(self):
        
        # delete lists and dictionaries
        if hasattr(self, 'data_lines'):      del self.data_lines
        if hasattr(self, 'data_lines_old'):  del self.data_lines_old
        
        # kill buttons and frame
        try:
            for child in self.fetch_data_tab.winfo_children():
                child.destroy()
            self.fetch_data_tab.destroy()
        except Exception:
            pass
        
    # ======================================================================= #
    def _check_condition(self, data, string):
        """Check whether a run satisfies the condition given as a string"""
        
        # determine what variable is being tested
        keyvars = np.array(list(KEYVARS.keys()))
        keylens = [len(k) for k in keyvars]
        keyvars = keyvars[np.argsort(keylens)[::-1]]
        
        found = False
        for key in keyvars:
            if key in string:
                found = True
                break
        
        if not found:
            msg = 'Variable not recognized in "%s"' % string
            messagebox.showerror('Filter', msg)
            raise RuntimeError(msg)
        
        # replace key with value
        val, err = data.get_values(KEYVARS[key])
        string = string.replace(key, str(val))
        
        # evaluate
        return eval(string)
    
    # ======================================================================= #
    def _do_check_all(self, state, var, box):
        """
            Force all tickboxes of a given type to be in a given state, assuming 
            the tickbox is active
        """
        
        self.logger.info('Changing state of all %s tickboxes to %s', var, state)
        for dline in self.data_lines.values():
            
            # check if line is selected
            if not dline.check_state.get() and var != 'check_state':
                continue
            
            # check if tickbox is object variable
            if hasattr(dline, box):
                
                # check if tickbox is disabled
                if str(getattr(dline, box)['state']) == 'disabled':
                    continue
                    
            # set value
            getattr(dline, var).set(state)
            
            # run check for other items
            if hasattr(dline, 'do_'+var):
                getattr(dline, 'do_'+var)()
    
    # ======================================================================= #
    def canvas_scroll(self, event):
        """Scroll canvas with files selected."""
        if event.num == 4:
            self.data_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.data_canvas.yview_scroll(1, "units")
    
    # ======================================================================= #
    def check_all(self):  
        self._do_check_all(self.check_state.get(), 'check_state', 'None')
        
    def check_all_data(self):  
        self._do_check_all(self.check_state_data.get(), 'check_data', 'None')
        
    def check_all_fit(self):  
        self._do_check_all(self.check_state_fit.get(), 'check_fit', 'draw_fit_checkbox')
    
    def check_all_res(self):  
        self._do_check_all(self.check_state_res.get(), 'check_res', 'draw_res_checkbox')    
        
    # ======================================================================= #
    def config_canvas(self, event):
        """Alter scrollable region based on canvas bounding box size. 
        (changes scrollbar properties)"""
        self.data_canvas.configure(scrollregion=self.data_canvas.bbox("all"))
    
    # ======================================================================= #
    def config_dataline_frame(self, event):
        """Alter size of contained frame in canvas. Allows for inside window to 
        be resized with mouse drag""" 
        self.data_canvas.itemconfig(self.canvas_frame_id, width=event.width)
        
    # ======================================================================= #
    def draw_all(self, figstyle, ignore_check=False):
        """
            Draw all data in data lines
            
            figstyle: one of "data", "fit", or "param" to choose which figure 
                    to draw in
            ignore_check: draw all with no regard to whether the run has been 
                    selected
        """
        
        self.logger.debug('Drawing all data (ignore check: %s)', ignore_check)
        
        # condense drawing into a funtion
        def draw_lines():
            for k, line in self.data_lines.items():
                if line.check_state.get() or ignore_check:
                    line.draw(figstyle)
                
        # get draw style
        style = self.bfit.draw_style.get()
        self.logger.debug('Draw style: "%s"',  style)
        
        # make new figure, draw stacked
        if style == 'stack':
            draw_lines()
            
        # overdraw in current figure, stacked
        elif style == 'redraw':
            self.bfit.draw_style.set('stack')
            
            if self.bfit.plt.plots[figstyle]:
                self.bfit.plt.clf(figstyle)
            
            draw_lines()
            self.bfit.draw_style.set('redraw')
            
        # make new figure, draw single
        elif style == 'new':
            self.bfit.draw_style.set('stack')
            self.bfit.plt.figure(figstyle)
            draw_lines()
            self.bfit.draw_style.set('new')
        else:
            s = "Draw style not recognized"
            messagebox.showerror(message=s)
            self.logger.error(s)
            raise ValueError(s)
    
        # remove legned if too many drawn values
        n_selected = sum([d.check_state.get() for d in self.data_lines.values()])
        if n_selected > self.bfit.legend_max_draw:
            
            try:
                self.bfit.plt.gca(figstyle).get_legend().remove()
            except AttributeError:
                pass
            else:
                self.bfit.plt.tight_layout(figstyle)
        
    # ======================================================================= #
    def export(self, directory=None):
        """Export all data files as csv"""
        
        # filename
        filename = self.bfit.fileviewer.default_export_filename
        if not filename: return
        self.logger.info('Exporting to file %s', filename)
        
        if directory is None:
            try:
                filename = os.path.join(filedialog.askdirectory(), filename)
            except TypeError:
                pass
        else:
            filename = os.path.join(directory, filename)
        
        # get data and write
        for k in self.bfit.data.keys():
            d = self.bfit.data[k]
            omit = d.omit.get()
            if omit == self.bin_remove_starter_line:    omit = ''
            self.bfit.export(d, filename%(d.year, d.run), rebin=d.rebin.get(), 
                             omit=omit)
        self.logger.debug('Success.')
        
    # ======================================================================= #
    def filter_runs(self):
        """Remove or select runs based on filter conditions"""
        
        # parse input string
        string = self.text_filter.get('1.0', END)
        lines = [l for l in string.split('\n') if l]
        
        # iterate on fetched data
        data_keep = []
        
        for k, d in self.bfit.data.items():
            
            # check conditions
            satisfy = all([self._check_condition(d, line) for line in lines])
            if satisfy:
                data_keep.append(k)
            
        # do filtering by selection
        if self.filter_opt.get() == 'activate':
            for k, d in self.bfit.data.items():
                d.check_state.set(k in data_keep)
                
        elif self.filter_opt.get() == 'remove':
            keys = tuple(self.data_lines.keys())
            for k in keys:
                if k not in data_keep:
                    self.data_lines[k].degrid()
    
    # ======================================================================= #
    def get_data(self):
        """Split data into parts, and assign to dictionary."""
        
        self.logger.debug('Fetching runs')
    
        # make list of run numbers, replace possible deliminators
        try:
            run_numbers = self.string2run(self.run.get())
        except ValueError:
            self.logger.exception('Bad run number string')
            raise ValueError('Bad run number string')
            
        # get list of merged runs
        merged_runs = self.get_merged_runs(self.run.get())
            
        # get the selected year
        year = int(self.year.get())
        
        # get data
        all_data = {}
        s = ['Failed to open run']
        for r in run_numbers:
            
            # read from archive
            try:
                all_data[r] = bdata(r, year=year)
            except (RuntimeError, ValueError):
                s.append("%d (%d)" % (r, year))
                    
        # print error message
        if len(s)>1:
            s = '\n'.join(s)
            print(s)
            self.logger.warning(s)
            messagebox.showinfo(message=s)
        
        # merge runs
        new_data = []
        for merge in merged_runs: 
            
            # collect data
            dat_to_merge = []
            for r in merge: 
                dat_to_merge.append(all_data.pop(r))
            
            # make bjoined object
            new_data.append(bmerged(dat_to_merge))
            
        new_data.extend(list(all_data.values()))
        
        # update object data lists
        data = {}
        for new_dat in new_data:
            
            # get key for data storage
            runkey = self.bfit.get_run_key(new_dat)

            # update data
            if runkey in self.bfit.data.keys():
                self.bfit.data[runkey].read()
                
            # new data
            else:
                data[runkey] = fitdata(self.bfit, new_dat)
    
        # check that data is all the same runtype
        run_types = [d.mode for d in self.bfit.data.values()]
        run_types = run_types + [d.mode for d in data.values()]
        
        # check for equivalent run modes
        selected_mode = [run_types[0]]
        for equiv in self.equivalent_modes:
            if selected_mode[0] in equiv:
                selected_mode = equiv
                break
        
        # different run types: select all runs of same type
        if not all([r in selected_mode for r in run_types]):
            
            # unique run modes
            run_type_unique = np.unique(run_types)
            
            # message for multiple run modes
            message = "Multiple run types detected:\n("
            message += ', '.join(run_type_unique)
            message += ')\n\nSelecting ' + ' and '.join(selected_mode) + ' runs.'
            messagebox.showinfo(message=message)
            
        # get only run_types[0]
        self.logger.debug('Fetching runs of mode %s', selected_mode)
        for k in tuple(data.keys()):
            if data[k].mode in selected_mode:
                self.bfit.data[k] = data[k]
            else:
                del data[k]
        
        # get runmode
        try:
            self.runmode = selected_mode
        except IndexError:
            s = 'No valid runs detected.'
            messagebox.showerror(message=s)
            self.logger.warning(s)
            raise RuntimeError(s)
            
        self.runmode_label['text'] = self.runmode_relabel[self.runmode[0]]
        
        # get area
        area = [d.area for d in self.bfit.data.values()]
        area = ''.join(np.unique(area))
        
        # set asym type comboboxes
        self.bfit.set_asym_calc_mode_box(self.runmode[0], self, area)
        self.bfit.set_asym_calc_mode_box(self.runmode[0], self.bfit.fit_files, area)
        
        keys_list = list(self.bfit.data.keys())
        keys_list.sort()
        
        # make lines
        n = 1
        for r in keys_list:
            
            # new line
            if r not in self.data_lines.keys():
                
                if r in self.data_lines_old.keys():
                    self.data_lines[r] = self.data_lines_old[r]
                    self.data_lines[r].set_label()
                    del self.data_lines_old[r]
                else:
                    self.data_lines[r] = dataline(\
                                            bfit = self.bfit, \
                                            lines_list = self.data_lines, \
                                            lines_list_old = self.data_lines_old, 
                                            fetch_tab_frame = self.dataline_frame, \
                                            bdfit = self.bfit.data[r], \
                                            row = n)
            self.data_lines[r].grid(n)
            n+=1
            
        # remove old runs, modes not selected
        for r in tuple(self.data_lines.keys()):
            if self.data_lines[r].bdfit.mode not in self.runmode:
                self.data_lines[r].degrid()
            
        # set nbm variable
        self.set_nbm()
        
        self.logger.info('Fetched runs %s', list(data.keys()))
        
    # ======================================================================= #
    def get_merged_runs(self, string):
        """
            Parse string, return list of lists of run numbers corresponding to 
            the data to merge
        """
        
        # find plus locations
        idx_plus = [m.start() for m in re.finditer(r'\+', string)]

        # remove spaces around plus
        for i in idx_plus[::-1]:
            if string[i+1] == ' ':
                string = string[:i+1]+string[i+2:]
            if string[i-1] == ' ':
                string = string[:i-1]+string[i:]
            
        # clean input
        string = re.sub('[, ;]', ' ', string)

        # add brackets
        string = ' '.join(['[%s]' % s if '+' in s else s for s in string.split()])

        # remove plusses
        string = re.sub(r'\+', ' ', string)

        # get strings for merging
        merge_strings = [*re.findall(r'\[(.*?)\]', string), 
                         *re.findall(r'\((.*?)\)', string), 
                         *re.findall(r'\{(.*?)\}', string)]

        
        # split up the input string by brackets
        merge_strings = [*re.findall(r'\[(.*?)\]', string), 
                         *re.findall(r'\((.*?)\)', string), 
                         *re.findall(r'\{(.*?)\}', string)]

        # get the run numbers in each of the merged string inputs
        merge_runs = [self.string2run(s) for s in merge_strings]
        
        return merge_runs
        
    # ======================================================================= #
    def history_set(self, x):
        """
            Set the history entry as the current fetch string
        """
        
        idx = self.listbox_history.curselection() 
        if not idx:
            on_focusout_fn(0)
            return 
            
        item = self.listbox_history.get(idx)
        self.listbox_history.delete(idx)
        self.listbox_history.insert(0, item)
        self.entry_run.delete(0, END)
        self.entry_run.insert(0, item)
        self.history_hide()
        self.entry_run.focus_set()
        
    # ======================================================================= #
    def history_show(self, x=None):
        """
            Show list widget with input history
        """
        if self.listbox_history.size()>0:
            self.listbox_history.config(height=self.listbox_history.size())
            x = self.entry_run.winfo_x()
            y = self.entry_run.winfo_y()
            dx = self.entry_run.winfo_width()
            self.listbox_history.place(x=x+6, y=y+30, width=dx)
            self.listbox_history.lift()
            
    # ======================================================================= #
    def history_hide(self, event=None, obj=None):
        """
            Hide list widget with input history
        """

        # don't hide if mousing over history
        if obj == 'entry' and 0 < event.x < 800 and event.y > 0:
            return  
        
        # hide the history box    
        self.listbox_history.place_forget()
        string = self.run.get() 
        
        if string != self.listbox_history.get(0) and \
           string != self.run_number_starter_line:
            self.listbox_history.insert(0, string)
            
        if self.listbox_history.size()>self.nhistory:
            self.listbox_history.delete(END)            
    
    # ======================================================================= #
    def remove_all(self):
        """Remove all data files from self.data_lines"""
        
        self.logger.info('Removing all data files')
        del_list = []
        for r in self.data_lines.keys():
            if self.data_lines[r].check_state.get():
                del_list.append(self.data_lines[r])
        
        for d in del_list:
            d.degrid()
    
    # ======================================================================= #
    def return_binder(self):
        """Switch between various functions of the enter button. """
        
        # check where the focus is
        focus_id = self.bfit.root.focus_get()
        
        # run or year entry
        if focus_id in [self.entry_run, self.entry_year]:
            self.logger.debug('Focus is: run or year entry')
            self.get_data()
            self.history_hide()
        
        # check all box
        elif focus_id == self.check_all_box:
            self.logger.debug('Focus is: check all box')
            self.draw_all()
            
        # filter
        elif focus_id == self.text_filter:
            self.logger.debug('Focus is: text_filter')
            self.filter_runs()
            
        else:
            pass

    # ======================================================================= #
    def set_all(self, changed, *args):
        """Set a particular property for all checked items. """
        
        self.logger.info('Set all')
        data = self.bfit.data
        
        # check all file lines
        for dat in data.values():
            
            # if checked
            if dat.check_state.get():
                
                # rebin
                if changed == 'rebin':
                    try:
                        rebin = self.check_rebin.get()
                    except TclError:
                        rebin = 1
                        
                    dat.rebin.set(rebin)
                
                # omit bins
                elif changed == 'omit':
                    dat.omit.set(self.check_bin_remove.get())
                
                # omit scan
                elif changed == 'omit_scan':
                    dat.omit_scan.set(self.omit_state.get())
                
                # baseline corrections
                elif changed == 'base_bins':
                    try:
                        val = self.base_bins.get()
                    except TclError:
                        val = 1
                    dat.base_bins.set(val)
                    
    # ======================================================================= #
    def set_all_labels(self):
        """Set lable text in all items """
        
        self.logger.info('Setting all label text')
        
        # check all file lines
        for r in self.data_lines.keys():
            self.data_lines[r].set_label()
            
        for r in self.data_lines_old.keys():
            self.data_lines_old[r].set_label()

    # ======================================================================= #
    def set_nbm(self):
        """
            Set the nbm variable based on the run mode
        """
        
        # check if data
        if not hasattr(self, 'runmode'):
            return
        
        # check run mode
        mode = self.runmode[0]
        
        self.bfit.set_nbm(mode)
    
    # ======================================================================= #
    def show_filter_instructions(self):
        """Display popup with instructions on filtering"""
        
        # instructions
        msg = 'Write one boolean expression \nper line using the below '+\
              'variables. \n\n'+\
              'Runs which satisfy all expressions \nare kept/activated\n\n'
              
        # variables
        keys = sorted(KEYVARS.keys())
        values = [KEYVARS[k] for k in keys]
        max_keylen = max(tuple(map(len, keys)))
        
        lines = [k.ljust(max_keylen+2) + v for k, v in zip(keys, values)]
              
        msg += '     ' + ('\n     '.join(lines))
        
        # example
        ex = 'ex: "10 < BIAS < 15"'
        msg += '\n\n' + ex
        
        # make window
        win = Toplevel(self.bfit.mainframe)
        win.title('How to filter runs')
        self.bfit.set_icon(win)
        
        frame = ttk.Frame(win, pad=10, relief='sunken')
        frame.grid(column=0, row=0)
        ttk.Label(frame, text=msg, justify='left').grid(column=0, row=0, pady=5)
        ttk.Button(frame, text='Close', 
                   command=lambda: win.destroy()).grid(column=0, row=1, pady=5)
            
    # ======================================================================= #
    def string2run(self, string):
        """Parse string, return list of run numbers"""
        
        # standardize deliminators
        full_string = re.sub(r'[, ;+\[\]\(\)\{\}]', ' ', string)
        full_string = full_string.replace(':', '-')
        part_string = full_string.split()
        
        # get list of run numbers
        run_numbers = []
        for s in part_string:
            
            # select a range
            if '-' in s:
                
                # get runs in range
                try:
                    spl = s.split('-')
                    
                    # look for "range to current run"
                    if spl[1] == '':
                        
                        # look for latest run by run number
                        if int(spl[0]) < 45000:
                            dirloc = os.environ[self.bfit.bnmr_archive_label]
                        else:
                            dirloc = os.environ[self.bfit.bnqr_archive_label]
                            
                        runlist = glob.glob(os.path.join(dirloc, 
                                                         str(self.year.get()), 
                                                         '*.msr'))
                        spl[1] = max([int(os.path.splitext(os.path.basename(r))[0]) 
                                   for r in runlist])
                        
                    rn_lims = tuple(map(int, spl))
                    
                # get bad range first value
                except ValueError:
                    run_numbers.append(int(s.replace('-', '')))
                
                # get range of runs
                else:
                    rns = np.arange(rn_lims[0], rn_lims[1]+1).tolist()
                    run_numbers.extend(rns)
            
            # get single run
            else:
                run_numbers.append(int(s))
        
        # sort
        run_numbers.sort()
        self.logger.debug('Parsed "%s" to run numbers (len: %d) %s', string, 
                          len(run_numbers), run_numbers)
        
        if len(run_numbers) > self.max_number_fetched:
            raise RuntimeWarning("Too many files selected (max %d)." \
                                                    % self.max_number_fetched)
        return run_numbers
    
    # ======================================================================= #
    def toggle_all(self):
        """Toggle all tickboxes"""
        self.logger.info('Toggling all tickboxes')
        for k in self.data_lines.keys():
            state = not self.data_lines[k].check_state.get()
            self.data_lines[k].check_state.set(state)

    # ======================================================================= #
    def update_data(self):
        """
            Re-fetch all fetched runs.
            Update labels
        """
        
        self.logger.info('Updating data')
        
        # fetch
        for dat in self.bfit.data.values():
            dat.read()
            
        # update text
        for line in self.data_lines.values():
            line.set_check_text()
            line.update_label()
        
# =========================================================================== #
# =========================================================================== #
class dataline(object):
    """
        A line of objects to display run properties and remove bins and whatnot.
        
        bdfit:          fitdata object 
        bfit:           pointer to root 
        bin_remove:     StringVar for specifying which bins to remove in 1f runs
        check:          Checkbox for selection (related to check_state)
        check_data:     BooleanVar for specifying to draw data
        check_fit:      BooleanVar for specifying to draw fit
        check_res:      BooleanVar for specifying to draw residual
        check_state:    BooleanVar for specifying check state
        draw_fit_checkbox: Checkbutton linked to check_fit
        draw_res_checkbox: Checkbutton linked to check_res
        id:             Str key for unique idenfication
        label:          StringVar for labelling runs in legends
        label_entry:    Entry object for labelling runs in legends
        line_frame:     Frame that object is placed in
        lines_list:     dictionary of datalines
        lines_list_old: dictionary of datalines
        mode:           bdata run mode
        rebin:          IntVar for SLR rebin
        row:            position in list
        run:            bdata run number
        year:           bdata year
    """
        
    bin_remove_starter_line = '24 100-200 (bins)'
    
    # ======================================================================= #
    def __init__(self, bfit, lines_list, lines_list_old, fetch_tab_frame, bdfit, row):
        """
            Inputs:
                fetch_tab_frame: parent in which to place line
                bdfit: fitdata object corresponding to the file which is placed here. 
                row: where to grid this object
        """
        
        # get logger
        self.logger = logging.getLogger(logger_name)
        self.logger.debug('Initializing run %d (%d)', bdfit.run, bdfit.year)
    
        # variables
        self.bfit = bfit
        self.row = row
        
        # variables from fitdata object
        self.bdfit = bdfit
        bd = bdfit.bd
        
        self.bin_remove = bdfit.omit
        self.label = bdfit.label
        self.rebin = bdfit.rebin
        self.check_state = bdfit.check_state
        self.mode = bdfit.mode
        self.run =  bdfit.run
        self.year = bdfit.year
        self.lines_list = lines_list
        self.lines_list_old = lines_list_old
        self.id = bdfit.id
        self.bdfit.dataline = self
        
        self.check_data = bdfit.check_draw_data
        self.check_fit = bdfit.check_draw_fit
        self.check_res = bdfit.check_draw_res
        
        # build objects
        line_frame = Frame(fetch_tab_frame)
        line_frame.bind('<Enter>', self.on_line_enter)
        line_frame.bind('<Leave>', self.on_line_leave)
        
        label_label = ttk.Label(line_frame, text="Label:", pad=5)
        self.label_entry = Entry(line_frame, textvariable=self.label, \
                width=18)
                
        remove_button = ttk.Button(line_frame, text='Remove', \
                command=self.degrid, pad=1)
        draw_button = ttk.Button(line_frame, text='Draw', 
                                 command=lambda:self.draw(figstyle='data'), 
                                 pad=1)
        
        draw_data_checkbox = ttk.Checkbutton(line_frame, text='Data', 
                variable=self.check_data, onvalue=True, offvalue=False, pad=5, 
                command=self.do_check_data)
        
        self.draw_fit_checkbox = ttk.Checkbutton(line_frame, text='Fit', 
                variable=self.check_fit, onvalue=True, offvalue=False, pad=5, 
                state=DISABLED, command=self.do_check_fit)
        
        self.draw_res_checkbox = ttk.Checkbutton(line_frame, text='Res', 
                variable=self.check_res, onvalue=True, offvalue=False, pad=5, 
                state=DISABLED, command=self.do_check_res)
        
        rebin_label = ttk.Label(line_frame, text="Rebin:", pad=5)
        rebin_box = Spinbox(line_frame, from_=1, to=100, width=3, \
                            textvariable=self.rebin)
        self.rebin.set(self.bfit.fetch_files.check_rebin.get())
                
        self.check_state.set(bfit.fetch_files.check_state.get())
        self.check = ttk.Checkbutton(line_frame, variable=self.check_state, \
                onvalue=True, offvalue=False, pad=5)
         
        self.set_check_text()
        
        # add button for data prep
        button_prep_data = ttk.Button(line_frame, text='Prep Data', 
                                      command=lambda : popup_prepare_data(self.bfit, self.bdfit), 
                                      pad=1)
         
        # add grey text to label
        self.set_label()
                
        # grid
        c = 1
        self.check.grid(column=c, row=0, sticky=E); c+=1
        button_prep_data.grid(column=c, row=0, sticky=E); c+=1
        rebin_label.grid(column=c, row=0, sticky=E); c+=1
        rebin_box.grid(column=c, row=0, sticky=E); c+=1
        label_label.grid(column=c, row=0, sticky=E); c+=1
        self.label_entry.grid(column=c, row=0, sticky=E); c+=1
        draw_data_checkbox.grid(column=c, row=0, sticky=E); c+=1
        self.draw_fit_checkbox.grid(column=c, row=0, sticky=E); c+=1
        self.draw_res_checkbox.grid(column=c, row=0, sticky=E); c+=1
        draw_button.grid(column=c, row=0, sticky=E); c+=1
        remove_button.grid(column=c, row=0, sticky=E); c+=1
        
        # resizing
        fetch_tab_frame.grid_columnconfigure(0, weight=1)   # big frame
        for i in (3, 5, 7):
            line_frame.grid_columnconfigure(i, weight=100)    # input labels
        for i in (4, 6, 8):
            line_frame.grid_columnconfigure(i, weight=1)  # input fields
        
        # passing
        self.line_frame = line_frame
                
    # ======================================================================= #
    def __del__(self):
        
        # kill buttons and frame
        try:
            for child in self.line_frame.winfo_children():
                child.destroy()
        except Exception:
            pass
            
    # ======================================================================= #
    def grid(self, row):
        """Re-grid a dataline object so that it is in order by run number"""
        self.row = row
        self.line_frame.grid(column=0, row=row, columnspan=2, sticky=(W, N))
        self.line_frame.update_idletasks()
        self.bfit.data[self.id] = self.bdfit
        self.set_check_text()
        
    # ======================================================================= #
    def degrid(self):
        """Hide displayed dataline object from file selection. """
        
        self.logger.info('Degridding run %s', self.id)
        
        # degrid
        self.line_frame.grid_forget()
        self.line_frame.update_idletasks()
        
        self.lines_list_old[self.id] = self.lines_list[self.id]
        del self.lines_list[self.id]
        del self.bfit.data[self.id]
        
        # uncheck the fit
        self.check_fit.set(False)
        self.draw_fit_checkbox.config(state='disabled')
        
        # repopulate fit files tab
        self.bfit.fit_files.populate()
        
        # remove data from storage
        if len(self.lines_list) == 0:
            ff = self.bfit.fetch_files
            ff.runmode_label['text'] = ''
                
    # ======================================================================= #
    def do_check_data(self):
        """Prevent resdiuals and fit/data checks from being true at the same time"""
        
        # get residual check value
        status = self.check_data.get()
            
        # set residuals
        if str(self.draw_res_checkbox['state']) == 'normal' and status:
            self.check_res.set(False)
    
    # ======================================================================= #
    def do_check_fit(self):
        """Prevent resdiuals and fit/data checks from being true at the same time"""
        
        # get residual check value
        status = self.check_fit.get()
            
        # set residuals
        if status:
            self.check_res.set(False)
    
    # ======================================================================= #
    def do_check_res(self):
        """Prevent resdiuals and fit/data checks from being true at the same time"""
        
        # get residual check value
        status = self.check_res.get()
            
        # set data and fit
        self.check_data.set(not status)
        self.check_fit.set(not status)    
    
    # ======================================================================= #
    def draw(self, figstyle):
        """
            Draw single data file.
            
            figstyle: one of "data", "fit", or "param" to choose which figure 
                    to draw in
        """
        
        # draw data
        if self.check_data.get():
            self.logger.info('Draw run %d (%d)', self.run, self.year)
                    
            # get new data file
            data = self.bfit.data[self.bfit.get_run_key(self.bdfit.bd)]
            data.read()
            
            # get data file run type
            d = self.bfit.fetch_files.asym_type.get()
            d = self.bfit.asym_dict[d]
            
            # draw
            data.draw(d, figstyle=figstyle, label=self.label.get())
            
        # draw fit
        if self.check_fit.get():
            if self.check_data.get():
                mode = self.bfit.draw_style.get()
                self.bfit.draw_style.set('stack')
                self.bdfit.draw_fit(unique=False, 
                                    asym_mode=self.bfit.get_asym_mode(self.bfit.fetch_files), 
                                    figstyle=figstyle)
                self.bfit.draw_style.set(mode)
            else:
                self.bdfit.draw_fit(figstyle=figstyle, 
                                    asym_mode=self.bfit.get_asym_mode(self.bfit.fetch_files))
                
        # draw residual
        if self.check_res.get():
            self.bdfit.draw_residual(figstyle=figstyle, 
                                     rebin=self.rebin.get())

    # ======================================================================= #
    def set_check_text(self):
        """Update the string for the check state box"""
        
        bdfit = self.bdfit
        
        # temperature
        try:
            self.temperature = int(np.round(bdfit.temperature.mean))
        except (ValueError, AttributeError):
            self.temperature = np.nan
            
        # field (Tesla)
        if bdfit.field > 0.1:
            self.field = np.around(bdfit.field, 2)
            
            try:
                field_text = "%3.2fT"%self.field
            except TypeError:
                field_text = ' '
        else:
            self.field = np.round(bdfit.field*1e4)
            
            try:
                field_text = "%3.0fG"%self.field
            except TypeError:
                field_text = ' '
        
        # bias
        self.bias = self.bdfit.bias
        try:
            bias_text = "%4.2fkV"%self.bias
        except TypeError:
            bias_text = ' '
        
        # duration 
        try: 
            duration_text = "%02d:%02d" % divmod(self.bdfit.duration, 60)
        except AttributeError:
            duration_text = ' '
        
        # set the text    
        if '+' in bdfit.id:
            unique_id = '%s+' % bdfit.id.split('+')[0]
        else:
            unique_id = '%s,' % bdfit.id
        
        
        T = '%3dK' % self.temperature if not np.isnan(self.temperature) else 'nan'
        
        info_str = "%s %s, %s, %s, %s" %  (unique_id, 
                                             T, field_text, 
                                             bias_text, duration_text)
        self.check.config(text=info_str)
    
    # ======================================================================= #
    def set_label(self):
        """Set default label text"""
        
        # get default label
        try:
            label = self.bfit.get_label(self.bfit.data[self.id])
        except KeyError:
            return
        
        # clear old text
        self.label_entry.delete(0, 'end')
        
        # set
        self.label_entry.insert(0, label)
        
        # make function to clear and replace with default text
        entry_fn_lab = partial(on_entry_click, text=label, 
                               entry=self.label_entry)
        on_focusout_fn_lab = partial(on_focusout, text=label, 
                                 entry=self.label_entry)
                                 
        # bindings
        self.label_entry.bind('<FocusIn>', entry_fn_lab)
        self.label_entry.bind('<FocusOut>', on_focusout_fn_lab)
        self.label_entry.config(foreground=colors.entry_grey)
        
    # ======================================================================= #
    def on_line_enter(self, *args):
        """Make the dataline grey on mouseover"""
        self.line_frame.config(bg=colors.focusbackground)
    
    # ======================================================================= #
    def on_line_leave(self, *args):
        """Make the dataline black on stop mouseover"""
        self.line_frame.config(bg=colors.background)

    # ======================================================================= #
    def update_label(self):
        """Set label unless values are user-defined"""
        
        if str(self.label_entry.config()['foreground'][4]) == colors.entry_grey:
            self.set_label()
