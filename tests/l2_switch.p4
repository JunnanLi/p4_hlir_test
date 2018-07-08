#include "includes/l2headers.p4"
#include "includes/l2parser.p4"

action hop_mac(egress_port) {
    //sub_hop_mac(egress_port);
    modify_field(switching_metadata.egress_port, egress_port);
    //modify_field(switching_metadata.ingress_port, ingress_port);
}

action sub_hop_mac(ingress_port){
    modify_field(switching_metadata.ingress_port, ingress_port);
}

action send_to_cpu() {
    modify_field(switching_metadata.cpu_tag, 1);
}


/* This should not be necessary if drop is allowed in table action specs */
action drop_pkt() {
    drop();
}

action no_operation() {
    no_op();
}

table mac_learning {
    reads {
        ethernet.srcAddr : exact;
        switching_metadata.ingress_port: exact;
    }
    actions {
      no_operation;
    }
}


table mac_switching {
    reads {
        ethernet.dstAddr : exact;
    }
    actions {
      drop_pkt;
      //sub_hop_mac;
      hop_mac;
    }
}

table src_mac {
    actions {
        send_to_cpu;
    }
}


 

control ingress {
    apply(mac_learning) {
        miss {
            apply(src_mac);
        }
    }
    apply(mac_switching);
}


// test of if_else condition
/*
control ingress {
    apply(mac_learning);
    if (switching_metadata.ingress_port > 4) {
        apply(src_mac);
    }
    apply(mac_switching);
}
*/

control egress {

}