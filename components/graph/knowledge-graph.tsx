"use client";

import React, { useMemo, useState } from "react";
import ReactFlow, { Background, Controls, MiniMap, Node, Edge, Handle, Position } from "reactflow";
import "reactflow/dist/style.css";

const nodeStyle = "rounded-2xl border border-white/10 bg-slate-950/90 px-4 py-3 text-white shadow-premium";

function IntelligenceNode({ data }: { data: { label: string; kind: string } }) {
  return (
    <div className={nodeStyle}>
      <Handle type="target" position={Position.Top} className="!bg-cyan-400" />
      <p className="text-[11px] uppercase tracking-[0.25em] text-cyan-200/70">{data.kind}</p>
      <p className="mt-1 text-sm font-semibold">{data.label}</p>
      <Handle type="source" position={Position.Bottom} className="!bg-cyan-400" />
    </div>
  );
}

const nodeTypes = { intelligence: IntelligenceNode };

export function KnowledgeGraph() {
  const [selected, setSelected] = useState<string>("Transaction A");

  const nodes: Node[] = useMemo(
    () => [
      { id: "1", type: "intelligence", position: { x: 80, y: 60 }, data: { label: "Customer A", kind: "Customer" } },
      { id: "2", type: "intelligence", position: { x: 360, y: 40 }, data: { label: "Device X9", kind: "Device" } },
      { id: "3", type: "intelligence", position: { x: 650, y: 60 }, data: { label: "Merchant Nova", kind: "Merchant" } },
      { id: "4", type: "intelligence", position: { x: 220, y: 220 }, data: { label: "Location SG", kind: "Location" } },
      { id: "5", type: "intelligence", position: { x: 520, y: 240 }, data: { label: "Fraud Case 447", kind: "Fraud Case" } },
      { id: "6", type: "intelligence", position: { x: 320, y: 380 }, data: { label: "Transaction A", kind: "Transaction" } }
    ],
    []
  );

  const edges: Edge[] = useMemo(
    () => [
      { id: "e1-2", source: "1", target: "2", animated: true },
      { id: "e2-3", source: "2", target: "3", animated: true },
      { id: "e1-4", source: "1", target: "4", animated: true },
      { id: "e4-5", source: "4", target: "5", animated: true },
      { id: "e5-6", source: "5", target: "6", animated: true }
    ],
    []
  );

  return (
    <section className="grid gap-5 xl:grid-cols-[1.4fr_0.6fr]">
      <div className="glass-card gradient-border h-[780px] overflow-hidden p-2">
        <ReactFlow nodes={nodes} edges={edges} nodeTypes={nodeTypes} fitView onNodeClick={(_, node) => setSelected(node.data.label)}>
          <Background color="rgba(255,255,255,0.08)" gap={26} />
          <Controls />
          <MiniMap zoomable pannable />
        </ReactFlow>
      </div>

      <div className="glass-card gradient-border p-5">
        <h3 className="text-lg font-semibold text-white">Node Details</h3>
        <div className="mt-4 rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Selected entity</p>
          <p className="mt-2 text-2xl font-semibold text-white">{selected}</p>
          <p className="mt-2 text-sm text-slate-400">Relationship trace linked across customer, device, merchant, and case memory.</p>
        </div>
        <div className="mt-4 space-y-3 text-sm text-slate-300">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Connection confidence: 97%</div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Risk propagation: High</div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">Memory cluster: MX-447</div>
        </div>
      </div>
    </section>
  );
}