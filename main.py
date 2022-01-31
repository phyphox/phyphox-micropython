import phyphoxBLE
import phyphoxBleExperiment
import time

def demo():
    # Name max length is 26 characters
    p = phyphoxBLE.PhyphoxBLE()
    
    A = phyphoxBleExperiment.PhyphoxBleExperiment()
    V = phyphoxBleExperiment.PhyphoxBleExperiment.View()
    G = phyphoxBleExperiment.PhyphoxBleExperiment.Graph()
    E = phyphoxBleExperiment.PhyphoxBleExperiment.Edit()
    I = phyphoxBleExperiment.PhyphoxBleExperiment.InfoField()
    S = phyphoxBleExperiment.PhyphoxBleExperiment.Separator()
    Val = phyphoxBleExperiment.PhyphoxBleExperiment.Value()
    V.setLabel("firstView")
    I.setInfo("Just a test")
    S.setHeight(0.7)
    G.setLabelX("tmpLabel")
    G.setXMLAttribute("unitY=\"m\"")
    G.setChannel(1, 2)
    G.setLabel("test")
    V.addElement(G)
    V.addElement(S)
    V.addElement(E)
    V.addElement(I)
    V.addElement(Val)
    A.addView(V)
    
    p.start(device_name="a  long name", exp_pointer=A)
    
    #p.start("a long name")
    p.when_subscription_received()
    
    i = 0
    while True:
        #a=p.read_array(3)
        #print(a)
        if p.is_connected():
            # Short burst of queued notifications.
            """
            for _ in range(3):
                p.write(i,i/7,2*i)
                i += 1
            """
        time.sleep_ms(2000)
            


if __name__ == "__main__":
    demo()


