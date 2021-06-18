import java.util.*;

public class Connect4AI extends AIModule
{
	int player;
	int opponent;
	int maxDepth = 1;
	int bestMoveSeen;
	
	ArrayList<Integer> order = new ArrayList<Integer>(Arrays.asList(3,2,4,1,5,0,6));

	

    // Our agent is making its move here
	public void getNextMove(final GameStateModule game)
	{
        player = game.getActivePlayer();
        opponent = (game.getActivePlayer() == 1?2:1);

		//begin recursion when the terminate=false (we have enough time)
		while(!terminate){
			maxvalue(game, 0, player, Integer.MIN_VALUE, Integer.MAX_VALUE);
			if(!terminate) chosenMove=bestMoveSeen;
			maxDepth++; // iterative deepening
		}

		if(game.canMakeMove(chosenMove)) {
			game.makeMove(chosenMove);
			maxDepth=1;

			
		}
	}

	private int maxvalue(final GameStateModule state, int depth, int playerID, int alpha, int beta){
		int alpha1=alpha;
		int beta1=beta;
		if(terminate) return 0;
		if (depth >= maxDepth | state.isGameOver()) return eval(state);
		int bestV=Integer.MIN_VALUE;
		int v=Integer.MIN_VALUE;
		depth++;
		int maxV=Integer.MIN_VALUE;
		
		for(int j=0; j<order.size(); j++){
			int i=order.get(j);
			if(!state.canMakeMove(i)) continue;
			state.makeMove(i);
			int min=minvalue(state, depth, opponent, alpha1, beta1);
			v=Math.max(v, min);
			state.unMakeMove();
			if(v>maxV){
				maxV=v;
				if(depth==1){
					bestMoveSeen=i;
				}
			}
			if (v>=beta1){
				return v;
			}
			alpha1=Math.max(alpha1,v);
			
		}
		return v;
	}

	private int minvalue(final GameStateModule state, int depth, int playerID, int alpha, int beta){
		int alpha1=alpha;
		int beta1=beta;
		if(terminate) return 0;
		if (depth >= maxDepth | state.isGameOver()) return eval(state);
		int v=Integer.MAX_VALUE;
		depth++;
		
		for(int j=0; j<order.size(); j++){
			int i=order.get(j);
			if(!state.canMakeMove(i)) continue;
			state.makeMove(i);
			v=Math.min(v,maxvalue(state, depth, player, alpha1, beta1));
			state.unMakeMove();
			if (v<=alpha1){
				return v;
			}
			beta1=Math.min(beta1,v);
			
		}
		return v;
	}

    private class Node{
    	Node(final GameStateModule state, int column, int playerID){
    		column1 = column;
    		playerID1 = playerID;
    		state.makeMove(column1);
    		score1=eval(state);
    		state.unMakeMove();

    	}
    	public int getColumn(){
    		return column1;
    	}
    	public int getScore(){
    		return score1;
    	}
    	private int column1;
    	private int score1;
    	private int playerID1;
    }
	public class NodeComparator implements Comparator <Node> {

    	public int compare(Node d1, Node d2){       
        	return Integer.compare(d1.getScore(), d2.getScore());
    	}
	}
	

	private ArrayList<Integer> successor(final GameStateModule state, int playerID){
		ArrayList<Node> nodes= new ArrayList<Node>();
		ArrayList<Integer> result = new ArrayList<Integer>();
		for (int i=0; i<state.getWidth(); i++){
			if(state.canMakeMove(i)){
				Node k = new Node(state,i,playerID);
				nodes.add(k);
				}
			}
		Collections.sort(nodes, new NodeComparator());
		for(int j=0; j< nodes.size(); j++){
			Node temp = nodes.get(j);
			result.add(temp.getColumn());
		}
		return result;
		
	}
	

	private int eval(final GameStateModule state){

		int score=0;
		int index;
		int leftPlayer;
		int rightPlayer;
		int downPlayer;
		int nextPlayer;
		int dlPlayer;
		int ruPlayer;
		int ulPlayer;
		int rdPlayer;
		int leftBlock;
		int rightBlock;
		int downBlock;
		int dlBlock;
		int ruBlock;
		int ulBlock;
		int rdBlock;
		int height;
		int index1;
		int index2;
		int n=1; //reward
		int m=2; //punishment
		ArrayList<Integer> storePlayer= new ArrayList<Integer>(Arrays.asList(0,0,0,0,0,0));
		ArrayList<Integer> storeOpponent= new ArrayList<Integer>();
		boolean stackThreatPlayer=false;
		boolean stackThreatOpponent=false;
		boolean usefulThreatPlayer=false;
		boolean usefulThreatOpponent=false;


		// todo make stacked threats really bad
		// todo make it value the center more
		for(int i=0; i<state.getWidth(); i++){ // for each column

	    	// if full, continue
	    	if (!state.canMakeMove(i)) continue;



	    	// loop through empty squares in the column
	    	for(int j=state.getHeightAt(i); j>=0; j--){ // for each row
	    		
	    		storePlayer= new ArrayList<Integer>(Arrays.asList(0,0,0,0,0,0));
	    		storeOpponent= new ArrayList<Integer>(Arrays.asList(0,0,0,0,0,0));
	    		// ignore full squares
	    		if (state.getAt(i,j)!=0) break;

	    		// Calculate right/left threats
	    		// check left
	    		index=i-1;
	    		leftPlayer=state.getAt(i-1,j);
	    		leftBlock=0;
	    		if(leftPlayer!=0) {
	    			while(index>=0){
	    				nextPlayer=state.getAt(index,j);
	    				if(nextPlayer==leftPlayer){
	    					leftBlock++;
	    					index--;
	    				}
	    				else {
	    					break;
	    				}
	    			}
	    		}
	    		// check right
	    		index=i+1;
	    		rightPlayer=state.getAt(index,j);
	    		rightBlock=0;
	    		if(rightPlayer!=0){
	    			while(index<state.getWidth()){
	    				nextPlayer=state.getAt(index,j);
	    				if(nextPlayer==leftPlayer){
	    					rightBlock++;
	    					index++;
	    				}
	    				else {
	    					break;
	    				}
	    			}
	    		}

	    		// Calculate downward threats is unnecessary and messes things up
	    		// Calculate diagonal threats, positive slope, left (dl=down, left)
	    		index1=i-1;
	    		index2=j-1;
	    		dlPlayer=state.getAt(index1,index2);
	    		dlBlock=0;
	    		if(dlPlayer!=0){
	    			while(index1>=0 && index2>=0){
	    				nextPlayer=state.getAt(index1,index2);
	    				if(nextPlayer==dlPlayer){
	    					dlBlock++;
	    					index1--;
	    					index2--;
	    				}
	    				else break;
	    			}
	    		}

	    		// Calculate diagonal threats, positive slope, right (ru=right, up)
	    		index1=i+1;
	    		index2=j+1;
	    		ruPlayer=state.getAt(index1,index2);
	    		ruBlock=0;
	    		if(ruPlayer!=0){
	    			while(index1<state.getWidth() && index2<state.getHeight()){
	    				nextPlayer=state.getAt(index1,index2);
	    				if(nextPlayer==ruPlayer){
	    					ruBlock++;
	    					index1++;
	    					index2++;
	    				}
	    				else break;
	    			}
	    		}

	    		// Calculate diagonal threats, negative slope, left (ul=up, left)
	    		index1=i-1;
	    		index2=j+1;
	    		ulPlayer=state.getAt(index1,index2);
	    		ulBlock=0;
	    		if(ulPlayer!=0){
	    			while(index1>=0 && index2<state.getHeight()){
	    				nextPlayer=state.getAt(index1,index2);
	    				if(nextPlayer==ulPlayer){
	    					ulBlock++;
	    					index1--;
	    					index2++;
	    				}
	    				else break;
	    			}
	    		}

	    		// Calculate diagonal threats, negative slope, right (rd=right, down)
	    		index1=i+1;
	    		index2=j-1;
	    		rdPlayer=state.getAt(index1,index2);
	    		rdBlock=0;
	    		if(rdPlayer!=0){
	    			while(index1<state.getWidth() && index2>=0){
	    				nextPlayer=state.getAt(index1,index2);
	    				if(nextPlayer==rdPlayer){
	    					rdBlock++;
	    					index1++;
	    					index2--;
	    				}
	    				else break;
	    			}
	    		}

	    		


	    		// caluclate left/right scores
	    		if(leftBlock==3){
	    			if(leftPlayer==player) {
	    				score=score+n;
	    				storePlayer.set(j,storePlayer.get(j)+1);
	    			}
	    			if(leftPlayer==opponent) {
	    				score=score-m;
	    				storeOpponent.set(j,storeOpponent.get(j)+1);
	    			}
	    			
	    		}
	    		if(rightBlock==3){
	    			if(rightPlayer==player) {
	    				score=score+n;
	    				storePlayer.set(j,storePlayer.get(j)+1);
	    			}
	    			if(rightPlayer==opponent) {
	    				score=score-m;
	    				storeOpponent.set(j,storeOpponent.get(j)+1);
	    			}
	    			
	    		}
	    		if(((leftBlock+rightBlock)>=3) && (leftPlayer==rightPlayer)){
	    			if(leftPlayer==player) {
	    				score=score+n;
	    				storePlayer.set(j,storePlayer.get(j)+1);
	    			}
	    			if(leftPlayer==opponent) {
	    				score=score-m;
	    				storeOpponent.set(j,storeOpponent.get(j)+1);
	    			}
	    		}

	    		// calculate diagonal, positive scores
	    		
	    		if(dlBlock==3){
	    			if(dlPlayer==player){ 
	    				score=score+n;
	    				storePlayer.set(j,storePlayer.get(j)+1);
	    			}
	    			if(dlPlayer==opponent) {
	    				score=score-m;
	    				storeOpponent.set(j,storeOpponent.get(j)+1);
	    			}
	    		}
	    		if(ruBlock==3){
	    			if(ruPlayer==player) {
	    				score=score+n;
	    				storePlayer.set(j,storePlayer.get(j)+1);
	    			}
	    			if(ruPlayer==opponent) {
	    				score=score-m;
	    				storeOpponent.set(j,storeOpponent.get(j)+1);
	    			}
	    		}
	    		if(((dlBlock+ruBlock)>=3) && (dlPlayer==ruPlayer)){
	    			if(dlPlayer==player) {
	    				score=score+n;
	    				storePlayer.set(j,storePlayer.get(j)+1);
	    			}
	    			if(dlPlayer==opponent) {
	    				score=score-m;
	    				storeOpponent.set(j,storeOpponent.get(j)+1);
	    			}
	    		}

	    		// calculate diagonal, negative scores
	    		
	    		if(ulBlock==3){
	    			if(ulPlayer==player) {
	    				score=score+n;
	    				storePlayer.set(j,storePlayer.get(j)+1);
	    			}
	    			if(ulPlayer==opponent) {
	    				score=score-m;
	    				storeOpponent.set(j,storeOpponent.get(j)+1);
	    			}
	    		}
	    		if(rdBlock==3){
	    			if(rdPlayer==player) {
	    				score=score+n;
	    				storePlayer.set(j,storePlayer.get(j)+1);
	    			}
	    			if(rdPlayer==opponent) {
	    				score=score-m;
	    				storeOpponent.set(j,storeOpponent.get(j)+1);
	    			}
	    		}
	    		if(((ulBlock+rdBlock)>=3) && (ulPlayer==rdPlayer)){
	    			if(ulPlayer==player) {
	    				score=score+n;
	    				storePlayer.set(j,storePlayer.get(j)+1);
	    			}
	    			if(ulPlayer==opponent) {
	    				score=score-m;
	    				storeOpponent.set(j,storeOpponent.get(j)+1);
	    			}
	    		}


	    	}

	    	// loop through store list, look for stack threats.
	    	int last=0;
	    	for(int k =0; k<state.getHeight(); k++){
	    		int current = storePlayer.get(k);
	    		if (last==current && last!=0){
	    			stackThreatPlayer=true;
	    		}
	    		last=current;
	    	}

	    	int lastStore=0;
	    	for(int k =0; k<state.getHeight(); k++){
	    		int currentStore = storeOpponent.get(k);
	    		if (lastStore==currentStore && last!=0){
	    			stackThreatOpponent=true;
	    		}
	    		lastStore=currentStore;
	    	}

	    	//loop through store list, look for even/odd threats

	    	// if first player, you want threats on rows 0, 2, 4. Subtract even more points if opponent has 0,3,5. Didn't have an impact.
	    	if (player==1){
	    		if (storePlayer.get(0)>0) usefulThreatPlayer=true;
	    		if (storePlayer.get(2)>0) usefulThreatPlayer=true;
	    		if (storePlayer.get(4)>0) usefulThreatPlayer=true;
	    		if (storeOpponent.get(1)>0) usefulThreatOpponent=true;
	    		if (storeOpponent.get(3)>0) usefulThreatOpponent=true;
	    		if (storeOpponent.get(5)>0) usefulThreatOpponent=true;
	    	}
	    	if (player==2){
	    		if (storePlayer.get(1)>0) usefulThreatPlayer=true;
	    		if (storePlayer.get(3)>0) usefulThreatPlayer=true;
	    		if (storePlayer.get(5)>0) usefulThreatPlayer=true;
	    		if (storeOpponent.get(0)>0) usefulThreatOpponent=true;
	    		if (storeOpponent.get(2)>0) usefulThreatOpponent=true;
	    		if (storeOpponent.get(4)>0) usefulThreatOpponent=true;
	    	}
	    	
	    }

	    // weight score for endgame scenarios
	    	if (stackThreatPlayer) score=score+10;

	    	//TODO: WEIGHT LOWER i VALUE USEFUL THREATS AS MORE VALUABLE
	    	if (usefulThreatPlayer) score=score+10;
	    	
	    	if (stackThreatOpponent) score=Integer.MIN_VALUE;
	    	if (usefulThreatOpponent) score=Integer.MIN_VALUE;
	    	if(state.isGameOver()){
	    	if(state.getWinner()==player) score=Integer.MAX_VALUE;
	    	if(state.getWinner()==0) score=0;
	    	if(state.getWinner()==opponent) score=Integer.MIN_VALUE;
	    }
	    // TODO: value center more
	    return score;
	}
}
















