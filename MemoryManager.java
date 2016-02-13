
import java.awt.*;
import java.applet.*;
import java.util.*;
import java.awt.event.*;


public class MemoryManager extends Applet implements ActionListener
{
    static final int SIZE = 10;
    int [] memory = new int[SIZE];
    HeapManager m = new HeapManager(memory);
    Label [] labels = new Label[SIZE];
    TextField [] contents = new TextField[SIZE];
    TextField freeStart = new TextField();
    Panel p1 = new Panel();
    
    Hashtable vars = new Hashtable();
    java.awt.List varList = new java.awt.List(10);
    TextField input = new TextField(30);
    Button process = new Button("process");
    Label error = new Label();
    Panel p2 = new Panel();
    
    Panel p = new Panel();
    
    public void init()
    {
    for (int i=0; i<SIZE; i++){
        labels[i] = new Label("           " + i + ":");
        contents[i] = new TextField(""+ memory[i]);
    }
    
    p1.setLayout(new GridLayout(SIZE+1,2));
    for (int i=SIZE-1; i>=0; i--){
        p1.add(labels[i]);
        p1.add(contents[i]);
    }
    
    p1.add(new Label("freeStart:"));
    p1.add(freeStart);
    
    Panel p3 = new Panel();
    p3.setLayout(new GridLayout(4,1));
    p3.add(new Label("Memory calls:"));
    p3.add(input);
    process.addActionListener(this);
    p3.add(process);
    error.setForeground(Color.red);
    p3.add(error);
    p2.setLayout(new BorderLayout());
    p2.add("North",p3);
    p2.add("Center",varList);
    
    p.add(p2);
    p.add(p1);
    add(p);
    display();
    
    setBackground(Color.white);
    setSize(400,300);
    
    }
    
    public void actionPerformed(ActionEvent e)
    {
    StringTokenizer st = new StringTokenizer(input.getText()+";"," ",false);
    if (input.getText().substring(0,2).equals("m.")) // deallocate
    {
        String heap = st.nextToken(".");
        String op = st.nextToken("(;").substring(1);
        if (!op.equals("deallocate")) {error.setText("deallocate method expected"); return;}
        String var = st.nextToken(");").substring(1);
        if (!vars.containsKey(var)) {error.setText("illegal variable "+var); return;}
        m.deallocate(((Integer)vars.get(var)).intValue());
        vars.remove(var);
        varList.removeAll();
        Enumeration keys = vars.keys();
        while(keys.hasMoreElements()) {
        String key = (String)keys.nextElement();
        varList.add(key + ":  " + vars.get(key));
        }
    }
    else {  //allocate
        String var = st.nextToken("=;"); 
        if (!Character.isLetter(var.charAt(0))){error.setText("illegal variable "+var); return;}
        if (vars.containsKey(var)) {error.setText("variable " + var + " already allocated"); return;}
        String heap = st.nextToken(".;").substring(1);
        if (!heap.equals("m")) {error.setText("heap manager m expected"); return;}
        String op = st.nextToken("(;").substring(1);
        if (!op.equals("allocate")) {error.setText("allocate method expected"); return;}
        String val = st.nextToken(");").substring(1);
        int value=0;
        try{
        value = Integer.parseInt(val);
        }catch(NumberFormatException ex) {error.setText("illegal integer value"); return;}
        int loc =0;
        try {
        loc = m.allocate(value);
        }catch(OutOfMemoryError ex) {error.setText("Out of memory error"); return; }
        vars.put(var,new Integer(loc));
        varList.add(var + ":  " + loc);
    }
    error.setText("");
    display();
    }
    
    public void display()
    {
    freeStart.setText(""+m.freeStart);
    for (int i=0;i<SIZE; i++) {
        contents[i].setText(""+ memory[i]);
        if (memory[i]==0) contents[i].setText("");
        contents[i].setBackground(Color.gray);
    }
       
    // color allocated cells white 
    Enumeration keys = vars.keys();
    while(keys.hasMoreElements()) {
        String key = (String)keys.nextElement();
        int location = ((Integer)vars.get(key)).intValue();
        int size = memory[location-1];
        for (int i=0; i<size; i++) {
        contents[location-1+i].setBackground(Color.white);
        if (i!=0) contents[location-1+i].setText("");
        }
    }
    }
   
}
