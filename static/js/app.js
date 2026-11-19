async function requestHint(level){
 const output=document.getElementById('hint-output');
 if(!output)return;
 output.textContent='Consulting the case notes...';
 try{
  const response=await fetch('/hint',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({level})});
  const data=await response.json();
  output.textContent=data.hint || 'No hint available.';
 }catch(e){output.textContent='Hint service unavailable. Review your evidence.';}
}
