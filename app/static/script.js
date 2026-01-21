const socket = io();
const canvas = document.getElementById( "vizCanvas" );
const ctx = canvas.getContext( '2d' );
let currentStats = {};

socket.on( 'stats_update', ( data ) => {
  currentStats = data;
  draw();
});

function draw() {
  const speakers = Object.keys( currentStats );
  if ( speakers.length < 2 ) return;

  const n = speakers.length;
  const centerX = 300, centerY = 300, radius = 250;
  const total = Object.values( currentStats ).reduce( (a,b) => a+b, 0 );

  ctx.clearRect( 0, 0, 600, 600 );

  // Calculate points
  const points = speakers.map( (id,i) => {
    const angle = ( i * 2 * Math.PI ) / n - Math.PI / 2;
    return {
      x: centerX + radius * Math.cos( angle ),
      y: centerY + radius * Math.sin( angle ),
      weight: currentStats[id] / total,
      id: id
    };
  });

  // calculate 'mass center'
  let blobX = 0, blobY = 0;
  points.forEach( p => {
    blobX += p.x * p.weight;
    blobY += p.y * p.weight;
  });

  // draw background
  ctx.beginPath();
  points.forEach(( p, i ) => i === 0 ? ctx.moveTo( p.x, p.y ) : ctx.lineTo( p.x, p.y ));
  ctx.closePath();
  ctx.strokeStyle = '#444';
  ctx.stroke();

  // draw colours
  ctx.beginPath();
  points.forEach(( p, i ) => i === 0 ? ctx.moveTo( p.x, p.y ) : ctx.lineTo( p.x, p.y ));
  const grad = ctx.createRadialGradient( blobX, blobY, 10, blobX, blobY, radius );
  grad.addColorStop( 0, 'rgba(0, 255, 150, 0.8)' );
  grad.addColorStop( 1, 'rgba(0, 100, 255, 0.2)' );
  ctx.fillStyle = grad;
  ctx.fill();

  // speaker labels
  points.forEach( p => {
    ctx.fillStyle = "white";
    ctx.fillText( `${ p.id } (${ Math.round( p.weight*100 )}%)`,
      p.x - 20,
      p.y > centerY ? p.y + 20 : p.y - 10 );
  });
}
